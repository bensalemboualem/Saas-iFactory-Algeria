"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import {
  User,
  Key,
  Bell,
  Palette,
  Save,
  Trash2,
  Shield,
  CreditCard
} from "lucide-react"

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Paramètres</h2>
        <p className="text-muted-foreground mt-2">
          Gérez vos préférences et configurations
        </p>
      </div>

      <Tabs defaultValue="profile" className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="profile">Profil</TabsTrigger>
          <TabsTrigger value="api">Clés API</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="appearance">Apparence</TabsTrigger>
          <TabsTrigger value="billing">Facturation</TabsTrigger>
        </TabsList>

        {/* Profile Tab */}
        <TabsContent value="profile" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Informations Personnelles
              </CardTitle>
              <CardDescription>
                Mettez à jour vos informations de profil
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="firstName">Prénom</Label>
                  <Input id="firstName" placeholder="John" defaultValue="IAFactory" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="lastName">Nom</Label>
                  <Input id="lastName" placeholder="Doe" defaultValue="User" />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="john@example.com"
                  defaultValue="user@iafactory.pro"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="company">Entreprise (optionnel)</Label>
                <Input id="company" placeholder="Mon Entreprise" />
              </div>

              <Separator />

              <div className="flex justify-between">
                <Button variant="outline">Annuler</Button>
                <Button className="gap-2">
                  <Save className="h-4 w-4" />
                  Sauvegarder
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                Sécurité
              </CardTitle>
              <CardDescription>
                Gérez vos paramètres de sécurité
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="currentPassword">Mot de passe actuel</Label>
                <Input id="currentPassword" type="password" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="newPassword">Nouveau mot de passe</Label>
                <Input id="newPassword" type="password" />
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirmer le mot de passe</Label>
                <Input id="confirmPassword" type="password" />
              </div>

              <Separator />

              <Button className="w-full">Changer le mot de passe</Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* API Keys Tab */}
        <TabsContent value="api" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Key className="h-5 w-5" />
                Clés API des Générateurs
              </CardTitle>
              <CardDescription>
                Configurez vos propres clés API pour les générateurs IA
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {[
                { name: "Runway ML", env: "RUNWAY_API_KEY", status: "configured" },
                { name: "Luma AI", env: "LUMA_AI_API_KEY", status: "configured" },
                { name: "Kling AI", env: "KLING_AI_ACCESS_KEY", status: "configured" },
                { name: "Alibaba Qwen", env: "ALIBABA_DASHSCOPE_API_KEY", status: "configured" },
                { name: "Pika Labs", env: "PIKA_LABS_API_KEY", status: "configured" },
                { name: "MiniMax / Hailuo", env: "MINIMAX_API_KEY", status: "configured" },
                { name: "Stability AI", env: "STABILITY_API_KEY", status: "configured" },
                { name: "Replicate AI", env: "REPLICATE_API_TOKEN", status: "configured" },
                { name: "Together AI", env: "TOGETHER_API_KEY", status: "configured" },
                { name: "Fal.ai", env: "FAL_AI_API_KEY", status: "configured" },
              ].map((api) => (
                <div key={api.name} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <p className="font-medium">{api.name}</p>
                    <p className="text-sm text-muted-foreground">{api.env}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    {api.status === "configured" && (
                      <div className="flex items-center gap-1.5 text-xs text-accent">
                        <div className="h-2 w-2 rounded-full bg-accent" />
                        Configurée
                      </div>
                    )}
                    <Button variant="outline" size="sm">Modifier</Button>
                  </div>
                </div>
              ))}

              <div className="bg-muted/50 p-4 rounded-lg">
                <p className="text-sm text-muted-foreground">
                  💡 <strong>Note:</strong> Les clés API sont actuellement gérées au niveau serveur.
                  Cette interface permettra bientôt aux utilisateurs de configurer leurs propres clés.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notifications Tab */}
        <TabsContent value="notifications" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Bell className="h-5 w-5" />
                Préférences de Notifications
              </CardTitle>
              <CardDescription>
                Choisissez comment vous souhaitez être notifié
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {[
                {
                  title: "Génération terminée",
                  description: "Être notifié quand une vidéo est prête",
                  defaultChecked: true
                },
                {
                  title: "Quota faible",
                  description: "Alertes quand vos quotas sont presque épuisés",
                  defaultChecked: true
                },
                {
                  title: "Nouveaux générateurs",
                  description: "Être informé des nouveaux générateurs IA disponibles",
                  defaultChecked: false
                },
                {
                  title: "Conseils & astuces",
                  description: "Recevoir des recommandations pour améliorer vos vidéos",
                  defaultChecked: true
                },
                {
                  title: "Newsletter",
                  description: "Mises à jour mensuelles et nouvelles fonctionnalités",
                  defaultChecked: false
                },
              ].map((notif) => (
                <div key={notif.title} className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>{notif.title}</Label>
                    <p className="text-sm text-muted-foreground">{notif.description}</p>
                  </div>
                  <Switch defaultChecked={notif.defaultChecked} />
                </div>
              ))}

              <Separator />

              <Button className="w-full gap-2">
                <Save className="h-4 w-4" />
                Sauvegarder les préférences
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Appearance Tab */}
        <TabsContent value="appearance" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Palette className="h-5 w-5" />
                Apparence
              </CardTitle>
              <CardDescription>
                Personnalisez l'interface selon vos préférences
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Thème</Label>
                <Select defaultValue="light">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="light">Clair</SelectItem>
                    <SelectItem value="dark">Sombre</SelectItem>
                    <SelectItem value="system">Système</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Langue</Label>
                <Select defaultValue="fr">
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="fr">Français</SelectItem>
                    <SelectItem value="ar">العربية</SelectItem>
                    <SelectItem value="en">English</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Separator />

              <Button className="w-full gap-2">
                <Save className="h-4 w-4" />
                Sauvegarder
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Billing Tab */}
        <TabsContent value="billing" className="space-y-4 mt-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CreditCard className="h-5 w-5" />
                Plan & Facturation
              </CardTitle>
              <CardDescription>
                Gérez votre abonnement et paiements
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="p-6 bg-gradient-to-r from-primary/10 to-accent/10 rounded-lg border">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold">Plan Premium</h3>
                    <p className="text-sm text-muted-foreground">Accès illimité à tous les générateurs</p>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold">$0.00</p>
                    <p className="text-xs text-muted-foreground">/ mois</p>
                  </div>
                </div>

                <div className="space-y-2 mb-4">
                  <div className="flex items-center gap-2 text-sm">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>6,100+ vidéos gratuites/jour</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>10 générateurs IA premium</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <div className="h-1.5 w-1.5 rounded-full bg-accent" />
                    <span>Qualité jusqu'à 4K</span>
                  </div>
                </div>

                <Button variant="outline" className="w-full">
                  Mettre à niveau vers Enterprise
                </Button>
              </div>

              <div className="space-y-3">
                <h4 className="font-medium">Historique de facturation</h4>
                <div className="text-center py-8 text-muted-foreground text-sm">
                  Aucune facture pour le moment
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-destructive/50">
            <CardHeader>
              <CardTitle className="text-destructive">Zone Dangereuse</CardTitle>
              <CardDescription>
                Actions irréversibles sur votre compte
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between p-4 border border-destructive/50 rounded-lg">
                <div>
                  <p className="font-medium text-destructive">Supprimer le compte</p>
                  <p className="text-sm text-muted-foreground">
                    Supprimer définitivement votre compte et toutes vos données
                  </p>
                </div>
                <Button variant="destructive" size="sm" className="gap-2">
                  <Trash2 className="h-4 w-4" />
                  Supprimer
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
