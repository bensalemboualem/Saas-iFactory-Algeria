import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Sparkles, Video, TrendingUp, Zap } from "lucide-react"
import Link from "next/link"

export default function Home() {
  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Bienvenue sur Dzir IA Video Studio</h2>
        <p className="text-muted-foreground mt-2">
          Créez des vidéos professionnelles avec l'IA en quelques clics
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Générateurs Actifs</CardTitle>
            <Zap className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">10</div>
            <p className="text-xs text-muted-foreground">
              Runway, Luma AI, Kling AI, Alibaba...
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Quota Journalier</CardTitle>
            <TrendingUp className="h-4 w-4 text-accent" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">6,100</div>
            <p className="text-xs text-muted-foreground">
              Vidéos gratuites par jour
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Vidéos Créées</CardTitle>
            <Video className="h-4 w-4 text-chart-3" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">
              Commencez votre première création
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Qualité Moyenne</CardTitle>
            <Sparkles className="h-4 w-4 text-chart-4" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">85/100</div>
            <p className="text-xs text-muted-foreground">
              Score de qualité IA
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Featured Generators */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Générateurs Premium</CardTitle>
              <Badge variant="default">TOP 3</Badge>
            </div>
            <CardDescription>
              Les meilleurs générateurs pour vos vidéos professionnelles
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Runway Gen-4</p>
                <p className="text-sm text-muted-foreground">Qualité 95/100 • 4K</p>
              </div>
              <Badge className="bg-chart-1 text-white">Premium</Badge>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Luma AI Dream Machine</p>
                <p className="text-sm text-muted-foreground">Qualité 92/100 • 1080p</p>
              </div>
              <Badge className="bg-chart-2 text-white">Pro</Badge>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Kling AI Pro</p>
                <p className="text-sm text-muted-foreground">Qualité 90/100 • 1080p</p>
              </div>
              <Badge className="bg-chart-3 text-white">Pro</Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Démarrage Rapide</CardTitle>
              <Badge variant="outline">Guide</Badge>
            </div>
            <CardDescription>
              Créez votre première vidéo en 5 étapes simples
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground">
                  1
                </div>
                <p className="text-sm">Choisissez votre générateur IA</p>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground">
                  2
                </div>
                <p className="text-sm">Décrivez votre vidéo (prompt)</p>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground">
                  3
                </div>
                <p className="text-sm">Ajustez les paramètres (durée, style)</p>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground">
                  4
                </div>
                <p className="text-sm">Générez et suivez la progression</p>
              </div>
              <div className="flex items-center gap-2">
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground">
                  5
                </div>
                <p className="text-sm">Téléchargez votre vidéo HD</p>
              </div>
            </div>
            <Link href="/studio">
              <Button className="w-full gap-2">
                <Sparkles className="h-4 w-4" />
                Créer ma première vidéo
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
