import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/auth';
import prisma from '@/lib/prisma';

// Credit plans
const PLANS = {
  starter: { credits: 1000, priceDzd: 1990, name: 'Starter' },
  pro: { credits: 5000, priceDzd: 4990, name: 'Pro' },
  business: { credits: 20000, priceDzd: 14990, name: 'Business' },
  enterprise: { credits: 100000, priceDzd: 49990, name: 'Enterprise' },
};

const CREDIT_PACKS = [
  { credits: 500, priceDzd: 990 },
  { credits: 1000, priceDzd: 1790 },
  { credits: 2500, priceDzd: 3990 },
  { credits: 5000, priceDzd: 6990 },
  { credits: 10000, priceDzd: 12990 },
];

export async function POST(request: NextRequest) {
  try {
    const session = await auth();

    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Non authentifié' },
        { status: 401 }
      );
    }

    const userId = session.user.id;
    const { type, planId, credits: creditAmount } = await request.json();

    let amount: number;
    let credits: number;
    let description: string;

    if (type === 'plan' && planId) {
      const plan = PLANS[planId as keyof typeof PLANS];
      if (!plan) {
        return NextResponse.json(
          { error: 'Plan invalide' },
          { status: 400 }
        );
      }
      amount = plan.priceDzd;
      credits = plan.credits;
      description = `IAFactory Algeria - Plan ${plan.name}`;
    } else if (type === 'credits' && creditAmount) {
      const pack = CREDIT_PACKS.find(p => p.credits === creditAmount);
      if (!pack) {
        return NextResponse.json(
          { error: 'Pack de crédits invalide' },
          { status: 400 }
        );
      }
      amount = pack.priceDzd;
      credits = pack.credits;
      description = `IAFactory Algeria - ${credits} crédits`;
    } else {
      return NextResponse.json(
        { error: 'Type de paiement invalide' },
        { status: 400 }
      );
    }

    // Get user info
    const user = await prisma.user.findUnique({
      where: { id: userId },
      select: { email: true, name: true },
    });

    if (!user) {
      return NextResponse.json(
        { error: 'Utilisateur non trouvé' },
        { status: 404 }
      );
    }

    // Create Chargily checkout
    const chargilyApiKey = process.env.CHARGILY_API_KEY;
    const chargilyMode = process.env.CHARGILY_MODE || 'test';
    const baseUrl = chargilyMode === 'live'
      ? 'https://pay.chargily.net/api/v2'
      : 'https://pay.chargily.net/test/api/v2';

    const appUrl = process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000';

    const chargilyResponse = await fetch(`${baseUrl}/checkouts`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${chargilyApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount,
        currency: 'DZD',
        customer_name: user.name || 'Client',
        customer_email: user.email,
        description,
        success_url: `${appUrl}/payment/success`,
        failure_url: `${appUrl}/payment/failure`,
        webhook_url: `${appUrl}/api/payments/webhook`,
        locale: 'fr',
        metadata: {
          userId,
          type,
          planId: planId || null,
          credits,
        },
      }),
    });

    if (!chargilyResponse.ok) {
      const error = await chargilyResponse.json();
      console.error('Chargily error:', error);
      return NextResponse.json(
        { error: 'Erreur lors de la création du paiement' },
        { status: 500 }
      );
    }

    const checkout = await chargilyResponse.json();

    // Save transaction
    await prisma.transaction.create({
      data: {
        userId,
        chargilyId: checkout.id,
        checkoutUrl: checkout.checkout_url,
        amount,
        credits,
        plan: planId || null,
        status: 'pending',
      },
    });

    return NextResponse.json({
      checkoutUrl: checkout.checkout_url,
      checkoutId: checkout.id,
    });

  } catch (error) {
    console.error('Checkout error:', error);
    return NextResponse.json(
      { error: 'Erreur lors de la création du paiement' },
      { status: 500 }
    );
  }
}
