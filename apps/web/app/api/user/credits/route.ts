import { NextResponse } from 'next/server';
import { auth } from '@/auth';
import prisma from '@/lib/prisma';

// GET - Get user's credit balance
export async function GET() {
  try {
    const session = await auth();

    if (!session?.user?.id) {
      return NextResponse.json(
        { error: 'Non authentifié' },
        { status: 401 }
      );
    }

    const userId = session.user.id;

    const user = await prisma.user.findUnique({
      where: { id: userId },
      select: {
        credits: true,
        plan: true,
        _count: {
          select: { generations: true },
        },
      },
    });

    if (!user) {
      return NextResponse.json(
        { error: 'Utilisateur non trouvé' },
        { status: 404 }
      );
    }

    // Get this month's usage
    const startOfMonth = new Date();
    startOfMonth.setDate(1);
    startOfMonth.setHours(0, 0, 0, 0);

    const monthlyUsage = await prisma.generation.aggregate({
      where: {
        userId,
        createdAt: { gte: startOfMonth },
      },
      _sum: { credits: true },
      _count: true,
    });

    return NextResponse.json({
      credits: user.credits,
      plan: user.plan,
      totalGenerations: user._count.generations,
      monthlyUsage: {
        credits: monthlyUsage._sum.credits || 0,
        count: monthlyUsage._count,
      },
    });

  } catch (error) {
    console.error('Get credits error:', error);
    return NextResponse.json(
      { error: 'Erreur lors de la récupération' },
      { status: 500 }
    );
  }
}
