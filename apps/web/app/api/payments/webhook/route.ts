import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';
import prisma from '@/lib/prisma';

export async function POST(request: NextRequest) {
  try {
    // SECURITY: Reject if webhook secret not configured
    const secret = process.env.CHARGILY_SECRET;
    if (!secret) {
      console.error('CHARGILY_SECRET not configured - webhook disabled');
      return NextResponse.json(
        { error: 'Webhook not configured' },
        { status: 503 }
      );
    }

    const payload = await request.text();
    const signature = request.headers.get('signature') || '';

    // Verify webhook signature
    const expectedSignature = crypto
      .createHmac('sha256', secret)
      .update(payload)
      .digest('hex');

    if (!signature || signature !== expectedSignature) {
      console.error('Invalid webhook signature');
      return NextResponse.json(
        { error: 'Invalid signature' },
        { status: 401 }
      );
    }

    const event = JSON.parse(payload);

    // Handle checkout.paid event
    if (event.type === 'checkout.paid') {
      const { id, metadata } = event.data;
      const { userId, credits, planId } = metadata;

      // Find and update transaction
      const transaction = await prisma.transaction.findUnique({
        where: { chargilyId: id },
      });

      if (!transaction) {
        console.error('Transaction not found:', id);
        return NextResponse.json(
          { error: 'Transaction not found' },
          { status: 404 }
        );
      }

      // Update transaction and add credits in a single transaction
      await prisma.$transaction([
        prisma.transaction.update({
          where: { chargilyId: id },
          data: {
            status: 'paid',
            paymentMethod: event.data.payment_method || null,
          },
        }),
        prisma.user.update({
          where: { id: userId },
          data: {
            credits: { increment: credits },
            ...(planId ? { plan: planId } : {}),
          },
        }),
      ]);

      console.log(`Payment successful: ${credits} credits added to user ${userId}`);
    }

    // Handle failed/canceled/expired
    if (['checkout.failed', 'checkout.canceled', 'checkout.expired'].includes(event.type)) {
      const { id } = event.data;

      await prisma.transaction.update({
        where: { chargilyId: id },
        data: {
          status: event.type.replace('checkout.', ''),
        },
      });
    }

    return NextResponse.json({ received: true });

  } catch (error) {
    console.error('Webhook error:', error);
    return NextResponse.json(
      { error: 'Webhook processing failed' },
      { status: 500 }
    );
  }
}
