"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import {
  ChevronRight,
  ChevronLeft,
  Sparkles,
  Check,
  Wand2
} from "lucide-react"

const steps = [
  { id: 1, name: "Générateur", description: "Choisissez votre IA" },
  { id: 2, name: "Prompt", description: "Décrivez votre vidéo" },
  { id: 3, name: "Paramètres", description: "Configurez les options" },
  { id: 4, name: "Génération", description: "Créez votre vidéo" },
  { id: 5, name: "Résultat", description: "Téléchargez" },
]

export default function StudioPage() {
  const [currentStep, setCurrentStep] = useState(1)

  const nextStep = () => {
    if (currentStep < 5) setCurrentStep(currentStep + 1)
  }

  const prevStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1)
  }

  const progress = ((currentStep - 1) / (steps.length - 1)) * 100

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Studio de Création</h2>
        <p className="text-muted-foreground mt-2">
          Créez votre vidéo IA en 5 étapes simples
        </p>
      </div>

      {/* Progress Steps */}
      <div className="space-y-4">
        {/* Progress Bar */}
        <Progress value={progress} className="h-2" />

        {/* Steps Indicators */}
        <div className="grid grid-cols-5 gap-2">
          {steps.map((step) => (
            <div
              key={step.id}
              className={`flex flex-col items-center text-center cursor-pointer transition-all ${
                step.id === currentStep
                  ? "scale-105"
                  : step.id < currentStep
                  ? "opacity-70"
                  : "opacity-40"
              }`}
              onClick={() => setCurrentStep(step.id)}
            >
              <div
                className={`flex h-10 w-10 items-center justify-center rounded-full border-2 transition-colors ${
                  step.id < currentStep
                    ? "border-primary bg-primary text-primary-foreground"
                    : step.id === currentStep
                    ? "border-primary bg-background text-primary"
                    : "border-muted bg-background text-muted-foreground"
                }`}
              >
                {step.id < currentStep ? (
                  <Check className="h-5 w-5" />
                ) : (
                  <span className="text-sm font-semibold">{step.id}</span>
                )}
              </div>
              <div className="mt-2">
                <p className="text-sm font-medium">{step.name}</p>
                <p className="text-xs text-muted-foreground">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Content Area */}
      <Card className="min-h-[500px]">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Wand2 className="h-5 w-5 text-primary" />
                Étape {currentStep} : {steps[currentStep - 1].name}
              </CardTitle>
              <CardDescription className="mt-1">
                {steps[currentStep - 1].description}
              </CardDescription>
            </div>
            <Badge variant="outline">
              {currentStep} / {steps.length}
            </Badge>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Step 1: Generator Selection */}
          {currentStep === 1 && (
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Sélectionnez le générateur IA qui correspond le mieux à vos besoins
              </p>
              <Tabs defaultValue="premium" className="w-full">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="premium">Premium</TabsTrigger>
                  <TabsTrigger value="standard">Standard</TabsTrigger>
                  <TabsTrigger value="free">Gratuit</TabsTrigger>
                </TabsList>
                <TabsContent value="premium" className="space-y-3 mt-4">
                  <GeneratorCard
                    name="Runway Gen-4"
                    quality="95/100"
                    speed="180s"
                    price="$0.10/s"
                    features={["4K", "15s max", "Contrôles avancés"]}
                    tier="premium"
                  />
                  <GeneratorCard
                    name="Luma AI Dream Machine"
                    quality="92/100"
                    speed="120s"
                    price="$0.05/s"
                    features={["1080p", "10s max", "Haute qualité"]}
                    tier="premium"
                  />
                </TabsContent>
                <TabsContent value="standard" className="space-y-3 mt-4">
                  <GeneratorCard
                    name="Kling AI Pro"
                    quality="90/100"
                    speed="90s"
                    price="$0.03/s"
                    features={["1080p", "8s max", "Bon rapport qualité/prix"]}
                    tier="standard"
                  />
                  <GeneratorCard
                    name="Alibaba Qwen Video"
                    quality="85/100"
                    speed="70s"
                    price="$0.02/s"
                    features={["1080p", "6s max", "Rapide"]}
                    tier="standard"
                  />
                </TabsContent>
                <TabsContent value="free" className="space-y-3 mt-4">
                  <GeneratorCard
                    name="Hailuo AI 2.3"
                    quality="88/100"
                    speed="80s"
                    price="GRATUIT"
                    features={["1080p", "10s max", "30 vidéos/jour"]}
                    tier="free"
                  />
                  <GeneratorCard
                    name="Nano AI"
                    quality="72/100"
                    speed="35s"
                    price="GRATUIT"
                    features={["720p", "5s max", "50 vidéos/jour"]}
                    tier="free"
                  />
                </TabsContent>
              </Tabs>
            </div>
          )}

          {/* Step 2: Prompt */}
          {currentStep === 2 && (
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Étape 2 : Configuration du prompt (à venir)
              </p>
            </div>
          )}

          {/* Step 3: Settings */}
          {currentStep === 3 && (
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Étape 3 : Paramètres avancés (à venir)
              </p>
            </div>
          )}

          {/* Step 4: Generation */}
          {currentStep === 4 && (
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Étape 4 : Génération en cours (à venir)
              </p>
            </div>
          )}

          {/* Step 5: Result */}
          {currentStep === 5 && (
            <div className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Étape 5 : Résultat et téléchargement (à venir)
              </p>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex items-center justify-between pt-6 border-t">
            <Button
              variant="outline"
              onClick={prevStep}
              disabled={currentStep === 1}
            >
              <ChevronLeft className="h-4 w-4 mr-2" />
              Précédent
            </Button>

            <Button onClick={nextStep} disabled={currentStep === 5}>
              {currentStep === 4 ? "Générer" : "Suivant"}
              {currentStep === 4 ? (
                <Sparkles className="h-4 w-4 ml-2" />
              ) : (
                <ChevronRight className="h-4 w-4 ml-2" />
              )}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function GeneratorCard({
  name,
  quality,
  speed,
  price,
  features,
  tier
}: {
  name: string
  quality: string
  speed: string
  price: string
  features: string[]
  tier: "premium" | "standard" | "free"
}) {
  const tierColors = {
    premium: "bg-chart-1 text-white",
    standard: "bg-chart-2 text-white",
    free: "bg-chart-4 text-white"
  }

  return (
    <div className="flex items-center justify-between p-4 border rounded-lg hover:border-primary transition-colors cursor-pointer">
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-2">
          <h4 className="font-semibold">{name}</h4>
          <Badge className={tierColors[tier]}>{tier.toUpperCase()}</Badge>
        </div>
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <span>Qualité: {quality}</span>
          <span>•</span>
          <span>Vitesse: {speed}</span>
          <span>•</span>
          <span className="font-semibold text-foreground">{price}</span>
        </div>
        <div className="flex gap-2 mt-2">
          {features.map((feature, i) => (
            <Badge key={i} variant="outline" className="text-xs">
              {feature}
            </Badge>
          ))}
        </div>
      </div>
      <Button size="sm">Sélectionner</Button>
    </div>
  )
}
