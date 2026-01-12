"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Search,
  Sparkles,
  Rocket,
  Heart,
  TrendingUp,
  Briefcase,
  Palmtree,
  Film,
  Zap
} from "lucide-react"

interface Template {
  id: string
  title: string
  category: string
  description: string
  prompt: string
  generator: string
  duration: string
  quality: string
  style: string
  uses: number
  trending?: boolean
}

const templates: Template[] = [
  {
    id: "1",
    title: "Coucher de soleil cinématique",
    category: "nature",
    description: "Paysage époustouflant avec des couleurs vibrantes",
    prompt: "Cinematic sunset over mountain peaks, golden hour lighting, dramatic clouds, 4K quality, slow camera pan",
    generator: "Runway Gen-4",
    duration: "10s",
    quality: "4K",
    style: "Cinématique",
    uses: 1247,
    trending: true
  },
  {
    id: "2",
    title: "Ville futuriste nuit",
    category: "tech",
    description: "Métropole sci-fi avec néons et buildings",
    prompt: "Futuristic city at night, neon lights, flying cars, cyberpunk aesthetic, rain reflections, cinematic",
    generator: "Luma AI",
    duration: "8s",
    quality: "1080p",
    style: "Cyberpunk",
    uses: 892,
    trending: true
  },
  {
    id: "3",
    title: "Produit e-commerce",
    category: "business",
    description: "Présentation produit tournante fond blanc",
    prompt: "Product showcase on white background, 360 degree rotation, professional lighting, commercial quality",
    generator: "Kling AI",
    duration: "6s",
    quality: "1080p",
    style: "Commercial",
    uses: 2156,
    trending: false
  },
  {
    id: "4",
    title: "Voyage tropical",
    category: "travel",
    description: "Plage paradisiaque avec palmiers",
    prompt: "Tropical beach paradise, crystal clear water, palm trees swaying, blue sky, drone shot perspective",
    generator: "Hailuo AI 2.3",
    duration: "10s",
    quality: "1080p",
    style: "Naturel",
    uses: 654,
    trending: false
  },
  {
    id: "5",
    title: "Logo animation",
    category: "business",
    description: "Animation de logo professionnel",
    prompt: "Modern logo reveal animation, particles effect, corporate style, clean background, smooth transitions",
    generator: "Alibaba Qwen",
    duration: "5s",
    quality: "1080p",
    style: "Corporate",
    uses: 1543,
    trending: true
  },
  {
    id: "6",
    title: "Cuisine gastronomique",
    category: "food",
    description: "Présentation plat haute cuisine",
    prompt: "Fine dining food presentation, steam rising, garnish details, shallow depth of field, warm lighting",
    generator: "Nano AI",
    duration: "5s",
    quality: "720p",
    style: "Gastronomique",
    uses: 423,
    trending: false
  },
  {
    id: "7",
    title: "Action hero shot",
    category: "action",
    description: "Scène d'action explosive et dynamique",
    prompt: "Action hero walking away from explosion, slow motion, cinematic look, dramatic lighting, epic music vibe",
    generator: "Runway Gen-4",
    duration: "8s",
    quality: "4K",
    style: "Action",
    uses: 789,
    trending: true
  },
  {
    id: "8",
    title: "Nature zen",
    category: "nature",
    description: "Forêt apaisante avec brume matinale",
    prompt: "Peaceful forest morning, mist between trees, soft sunlight rays, birds flying, calm and serene atmosphere",
    generator: "Luma AI",
    duration: "10s",
    quality: "1080p",
    style: "Zen",
    uses: 567,
    trending: false
  }
]

const categories = [
  { id: "all", name: "Tous", icon: Sparkles },
  { id: "trending", name: "Tendances", icon: TrendingUp },
  { id: "nature", name: "Nature", icon: Palmtree },
  { id: "tech", name: "Tech", icon: Zap },
  { id: "business", name: "Business", icon: Briefcase },
  { id: "travel", name: "Voyage", icon: Rocket },
  { id: "food", name: "Food", icon: Heart },
  { id: "action", name: "Action", icon: Film },
]

export default function TemplatesPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")

  const filteredTemplates = templates.filter(template => {
    const matchesSearch = template.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === "all" ||
                           (selectedCategory === "trending" && template.trending) ||
                           template.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Templates de Vidéos</h2>
        <p className="text-muted-foreground mt-2">
          Utilisez des modèles prêts à l'emploi pour créer rapidement vos vidéos
        </p>
      </div>

      {/* Search Bar */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Rechercher un template par titre ou description..."
          className="pl-9"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Category Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {categories.map((category) => {
          const Icon = category.icon
          const isActive = selectedCategory === category.id
          return (
            <Button
              key={category.id}
              variant={isActive ? "default" : "outline"}
              size="sm"
              onClick={() => setSelectedCategory(category.id)}
              className="gap-2 whitespace-nowrap"
            >
              <Icon className="h-4 w-4" />
              {category.name}
              {category.id === "trending" && (
                <Badge variant="secondary" className="ml-1 h-5 px-1.5">
                  4
                </Badge>
              )}
            </Button>
          )
        })}
      </div>

      {/* Templates Grid */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {filteredTemplates.map((template) => (
          <Card key={template.id} className="overflow-hidden hover:shadow-lg transition-all group">
            {/* Preview Area */}
            <div className="relative aspect-video bg-gradient-to-br from-primary/20 to-accent/20 overflow-hidden">
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-6xl opacity-50">🎬</div>
              </div>
              {template.trending && (
                <Badge className="absolute top-2 left-2 bg-chart-4 text-white gap-1">
                  <TrendingUp className="h-3 w-3" />
                  Tendance
                </Badge>
              )}
              <div className="absolute bottom-2 right-2 bg-black/80 text-white text-xs px-2 py-1 rounded">
                {template.duration}
              </div>
            </div>

            <CardHeader>
              <CardTitle className="line-clamp-1">{template.title}</CardTitle>
              <CardDescription className="line-clamp-2">{template.description}</CardDescription>
            </CardHeader>

            <CardContent className="space-y-3">
              {/* Template Info */}
              <div className="flex items-center gap-2 text-xs text-muted-foreground flex-wrap">
                <Badge variant="outline">{template.generator}</Badge>
                <Badge variant="outline">{template.quality}</Badge>
                <Badge variant="outline">{template.style}</Badge>
              </div>

              {/* Prompt Preview */}
              <div className="bg-muted/50 p-3 rounded-lg">
                <p className="text-xs text-muted-foreground line-clamp-2">
                  {template.prompt}
                </p>
              </div>

              {/* Usage Stats */}
              <div className="flex items-center justify-between text-xs text-muted-foreground">
                <span>{template.uses.toLocaleString()} utilisations</span>
              </div>
            </CardContent>

            <CardFooter className="flex gap-2">
              <Button className="flex-1 gap-2" size="sm">
                <Sparkles className="h-4 w-4" />
                Utiliser ce template
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {filteredTemplates.length === 0 && (
        <Card className="p-12">
          <div className="flex flex-col items-center justify-center text-center">
            <div className="h-20 w-20 rounded-full bg-muted flex items-center justify-center mb-4">
              <Search className="h-10 w-10 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Aucun template trouvé</h3>
            <p className="text-muted-foreground mb-4">
              Essayez de modifier vos critères de recherche
            </p>
            <Button variant="outline" onClick={() => {
              setSearchQuery("")
              setSelectedCategory("all")
            }}>
              Réinitialiser les filtres
            </Button>
          </div>
        </Card>
      )}
    </div>
  )
}
