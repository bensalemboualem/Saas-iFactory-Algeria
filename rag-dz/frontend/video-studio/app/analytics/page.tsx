"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  TrendingUp,
  TrendingDown,
  Video,
  Clock,
  Zap,
  DollarSign,
  Activity,
  Award
} from "lucide-react"

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Analytics & Statistiques</h2>
        <p className="text-muted-foreground mt-2">
          Suivez vos performances et votre utilisation
        </p>
      </div>

      {/* Time Period Selector */}
      <Tabs defaultValue="7days" className="w-full">
        <TabsList>
          <TabsTrigger value="24h">24 heures</TabsTrigger>
          <TabsTrigger value="7days">7 jours</TabsTrigger>
          <TabsTrigger value="30days">30 jours</TabsTrigger>
          <TabsTrigger value="all">Tout</TabsTrigger>
        </TabsList>

        <TabsContent value="7days" className="space-y-6 mt-6">
          {/* Key Metrics */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Vidéos Générées</CardTitle>
                <Video className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">24</div>
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <TrendingUp className="h-3 w-3 text-accent" />
                  <span className="text-accent">+12%</span>
                  <span>vs semaine dernière</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Temps Moyen</CardTitle>
                <Clock className="h-4 w-4 text-chart-2" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">95s</div>
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <TrendingDown className="h-3 w-3 text-accent" />
                  <span className="text-accent">-8%</span>
                  <span>plus rapide</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Qualité Moyenne</CardTitle>
                <Award className="h-4 w-4 text-chart-3" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">87/100</div>
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <TrendingUp className="h-3 w-3 text-accent" />
                  <span className="text-accent">+3 pts</span>
                  <span>amélioration</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Coût Estimé</CardTitle>
                <DollarSign className="h-4 w-4 text-chart-4" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">$0.00</div>
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Badge variant="secondary" className="h-4 px-1.5 text-xs">
                    FREE
                  </Badge>
                  <span>quotas gratuits</span>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Usage by Generator */}
          <Card>
            <CardHeader>
              <CardTitle>Utilisation par Générateur</CardTitle>
              <CardDescription>Répartition des vidéos créées par générateur IA</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {[
                { name: "Runway Gen-4", count: 8, percentage: 33, color: "bg-chart-1" },
                { name: "Luma AI", count: 6, percentage: 25, color: "bg-chart-2" },
                { name: "Hailuo AI 2.3", count: 5, percentage: 21, color: "bg-chart-3" },
                { name: "Kling AI", count: 3, percentage: 13, color: "bg-chart-4" },
                { name: "Alibaba Qwen", count: 2, percentage: 8, color: "bg-chart-5" },
              ].map((gen) => (
                <div key={gen.name} className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">{gen.name}</span>
                    <span className="text-muted-foreground">
                      {gen.count} vidéos ({gen.percentage}%)
                    </span>
                  </div>
                  <div className="h-2 overflow-hidden rounded-full bg-muted">
                    <div
                      className={`h-full ${gen.color}`}
                      style={{ width: `${gen.percentage}%` }}
                    />
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Activité Récente</CardTitle>
                <CardDescription>Dernières générations de vidéos</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    {
                      title: "Paysage montagneux",
                      time: "Il y a 2 heures",
                      status: "success",
                      generator: "Runway Gen-4"
                    },
                    {
                      title: "Ville futuriste",
                      time: "Il y a 5 heures",
                      status: "success",
                      generator: "Luma AI"
                    },
                    {
                      title: "Océan calme",
                      time: "Il y a 8 heures",
                      status: "success",
                      generator: "Kling AI"
                    },
                    {
                      title: "Forêt enchantée",
                      time: "Hier",
                      status: "success",
                      generator: "Hailuo AI"
                    },
                  ].map((activity, i) => (
                    <div key={i} className="flex items-center gap-4">
                      <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10">
                        <Video className="h-4 w-4 text-primary" />
                      </div>
                      <div className="flex-1 space-y-1">
                        <p className="text-sm font-medium leading-none">{activity.title}</p>
                        <p className="text-xs text-muted-foreground">
                          {activity.generator} • {activity.time}
                        </p>
                      </div>
                      <Badge variant="outline" className="text-accent border-accent">
                        Succès
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Quotas & Limites</CardTitle>
                <CardDescription>Utilisation de vos quotas journaliers</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {[
                  {
                    name: "Hailuo AI 2.3",
                    used: 5,
                    total: 30,
                    color: "bg-chart-3"
                  },
                  {
                    name: "Nano AI",
                    used: 2,
                    total: 50,
                    color: "bg-chart-5"
                  },
                  {
                    name: "Runway Gen-4",
                    used: 8,
                    total: "∞",
                    color: "bg-chart-1",
                    premium: true
                  },
                ].map((quota) => (
                  <div key={quota.name} className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{quota.name}</span>
                        {quota.premium && (
                          <Badge className="h-4 px-1.5 text-xs">PREMIUM</Badge>
                        )}
                      </div>
                      <span className="text-muted-foreground">
                        {quota.used} / {quota.total}
                      </span>
                    </div>
                    {typeof quota.total === "number" && (
                      <div className="h-2 overflow-hidden rounded-full bg-muted">
                        <div
                          className={`h-full ${quota.color}`}
                          style={{ width: `${(quota.used / quota.total) * 100}%` }}
                        />
                      </div>
                    )}
                  </div>
                ))}

                <div className="pt-4 border-t">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">Quota total restant</span>
                    <span className="text-lg font-bold text-primary">6,073</span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    Réinitialisation dans 18h 24min
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Performance Insights */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-primary" />
                Insights & Recommandations
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex gap-3 p-3 bg-accent/10 rounded-lg border border-accent/20">
                <Activity className="h-5 w-5 text-accent flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-medium">Performance excellente</p>
                  <p className="text-xs text-muted-foreground">
                    Votre taux de réussite est de 100% cette semaine
                  </p>
                </div>
              </div>

              <div className="flex gap-3 p-3 bg-primary/10 rounded-lg border border-primary/20">
                <TrendingUp className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-medium">Générateur recommandé</p>
                  <p className="text-xs text-muted-foreground">
                    Runway Gen-4 offre le meilleur rapport qualité/temps pour vos projets
                  </p>
                </div>
              </div>

              <div className="flex gap-3 p-3 bg-chart-4/10 rounded-lg border border-chart-4/20">
                <Award className="h-5 w-5 text-chart-4 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-medium">Économies réalisées</p>
                  <p className="text-xs text-muted-foreground">
                    Vous avez économisé ~$15.60 en utilisant les quotas gratuits
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
