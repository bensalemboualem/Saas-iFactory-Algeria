"use client"

import { useState } from "react"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Search,
  Filter,
  Download,
  Share2,
  Trash2,
  Play,
  Clock,
  Sparkles
} from "lucide-react"

// Mock data - à remplacer par des vraies données de l'API
const mockVideos = [
  {
    id: "1",
    title: "Paysage montagneux au coucher du soleil",
    generator: "Runway Gen-4",
    thumbnail: "/placeholder-video-1.jpg",
    duration: "10s",
    quality: "4K",
    createdAt: "Il y a 2 heures",
    status: "completed",
    tier: "premium"
  },
  {
    id: "2",
    title: "Ville futuriste avec voitures volantes",
    generator: "Luma AI",
    thumbnail: "/placeholder-video-2.jpg",
    duration: "8s",
    quality: "1080p",
    createdAt: "Il y a 5 heures",
    status: "completed",
    tier: "premium"
  },
  {
    id: "3",
    title: "Océan calme avec dauphins sautants",
    generator: "Kling AI",
    thumbnail: "/placeholder-video-3.jpg",
    duration: "6s",
    quality: "1080p",
    createdAt: "Hier",
    status: "completed",
    tier: "standard"
  },
  {
    id: "4",
    title: "Forêt enchantée avec lucioles",
    generator: "Hailuo AI 2.3",
    thumbnail: "/placeholder-video-4.jpg",
    duration: "10s",
    quality: "1080p",
    createdAt: "Il y a 2 jours",
    status: "completed",
    tier: "free"
  },
  {
    id: "5",
    title: "Rue de Tokyo la nuit sous la pluie",
    generator: "Alibaba Qwen",
    thumbnail: "/placeholder-video-5.jpg",
    duration: "5s",
    quality: "1080p",
    createdAt: "Il y a 3 jours",
    status: "completed",
    tier: "standard"
  },
  {
    id: "6",
    title: "Galaxie spirale en rotation",
    generator: "Nano AI",
    thumbnail: "/placeholder-video-6.jpg",
    duration: "5s",
    quality: "720p",
    createdAt: "Il y a 1 semaine",
    status: "completed",
    tier: "free"
  },
]

export default function LibraryPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [filterBy, setFilterBy] = useState("all")
  const [sortBy, setSortBy] = useState("recent")

  const tierColors = {
    premium: "bg-chart-1",
    standard: "bg-chart-2",
    free: "bg-chart-4"
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Bibliothèque Vidéos</h2>
        <p className="text-muted-foreground mt-2">
          Gérez et téléchargez vos vidéos générées
        </p>
      </div>

      {/* Stats Bar */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <div className="text-2xl font-bold">6</div>
            <p className="text-xs text-muted-foreground">Vidéos totales</p>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <div className="text-2xl font-bold">45s</div>
            <p className="text-xs text-muted-foreground">Durée totale</p>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <div className="text-2xl font-bold">4</div>
            <p className="text-xs text-muted-foreground">Cette semaine</p>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">Générateurs utilisés</p>
          </CardHeader>
        </Card>
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Rechercher par titre, prompt ou générateur..."
            className="pl-9"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <Select value={filterBy} onValueChange={setFilterBy}>
          <SelectTrigger className="w-full sm:w-[180px]">
            <Filter className="h-4 w-4 mr-2" />
            <SelectValue placeholder="Filtrer par" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Tous les types</SelectItem>
            <SelectItem value="premium">Premium</SelectItem>
            <SelectItem value="standard">Standard</SelectItem>
            <SelectItem value="free">Gratuit</SelectItem>
          </SelectContent>
        </Select>

        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className="w-full sm:w-[180px]">
            <SelectValue placeholder="Trier par" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="recent">Plus récents</SelectItem>
            <SelectItem value="oldest">Plus anciens</SelectItem>
            <SelectItem value="quality">Qualité</SelectItem>
            <SelectItem value="duration">Durée</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Videos Grid */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {mockVideos.map((video) => (
          <Card key={video.id} className="overflow-hidden group hover:shadow-lg transition-all">
            {/* Thumbnail */}
            <div className="relative aspect-video bg-muted overflow-hidden">
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-4xl text-muted-foreground">🎬</div>
              </div>
              {/* Play overlay on hover */}
              <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <Button size="icon" variant="secondary" className="h-12 w-12 rounded-full">
                  <Play className="h-6 w-6" />
                </Button>
              </div>
              {/* Tier badge */}
              <Badge className={`absolute top-2 right-2 ${tierColors[video.tier]} text-white`}>
                {video.tier.toUpperCase()}
              </Badge>
              {/* Duration */}
              <div className="absolute bottom-2 right-2 bg-black/80 text-white text-xs px-2 py-1 rounded">
                {video.duration}
              </div>
            </div>

            <CardHeader className="pb-3">
              <h3 className="font-semibold line-clamp-1">{video.title}</h3>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Sparkles className="h-3 w-3" />
                <span>{video.generator}</span>
                <span>•</span>
                <span>{video.quality}</span>
              </div>
            </CardHeader>

            <CardFooter className="flex justify-between pt-0">
              <div className="flex items-center gap-1 text-xs text-muted-foreground">
                <Clock className="h-3 w-3" />
                <span>{video.createdAt}</span>
              </div>
              <div className="flex gap-1">
                <Button size="icon" variant="ghost" className="h-8 w-8">
                  <Download className="h-4 w-4" />
                </Button>
                <Button size="icon" variant="ghost" className="h-8 w-8">
                  <Share2 className="h-4 w-4" />
                </Button>
                <Button size="icon" variant="ghost" className="h-8 w-8 text-destructive hover:text-destructive">
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            </CardFooter>
          </Card>
        ))}
      </div>

      {/* Empty State (shown when no videos) */}
      {mockVideos.length === 0 && (
        <Card className="p-12">
          <div className="flex flex-col items-center justify-center text-center">
            <div className="h-20 w-20 rounded-full bg-muted flex items-center justify-center mb-4">
              <Sparkles className="h-10 w-10 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Aucune vidéo pour l'instant</h3>
            <p className="text-muted-foreground mb-4">
              Commencez à créer vos premières vidéos IA
            </p>
            <Button>
              <Sparkles className="h-4 w-4 mr-2" />
              Créer une vidéo
            </Button>
          </div>
        </Card>
      )}
    </div>
  )
}
