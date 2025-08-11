import {
    BarChart3,
    Building2,
    Calendar,
    CheckCircle,
    Download,
    Mail,
    Phone,
    Play,
    TrendingUp,
    Users,
    X,
    Zap
} from 'lucide-react'
import { useState } from 'react'
import { RecommendationProduct } from '../types/recommendation'
import { Badge } from './ui/badge'
import { Button } from './ui/button'

interface ProductDetailModalProps {
  isOpen: boolean
  onClose: () => void
  product: RecommendationProduct
}

type TabType = 'overview' | 'features' | 'success-stories' | 'resources'

export function ProductDetailModal({ isOpen, onClose, product }: ProductDetailModalProps) {
  const [activeTab, setActiveTab] = useState<TabType>('overview')

  if (!isOpen) return null

  const handleScheduleMeeting = () => {
    console.log(`Agendando reunião para produto: ${product.name}`)
  }

  const handleRequestDemo = () => {
    console.log(`Solicitando demo para produto: ${product.name}`)
  }

  const handleDownloadMaterial = (resourceUrl: string) => {
    console.log(`Download do material: ${resourceUrl}`)
  }

  const tabs = [
    { id: 'overview' as TabType, label: 'Visão Geral', icon: BarChart3 },
    { id: 'features' as TabType, label: 'Funcionalidades', icon: Zap },
    { id: 'success-stories' as TabType, label: 'Casos de Sucesso', icon: TrendingUp },
    { id: 'resources' as TabType, label: 'Recursos', icon: Download },
  ]

  const renderOverview = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-3">Sobre a Solução</h3>
        <p className="text-muted-foreground leading-relaxed">
          {product.detailedDescription || product.description}
        </p>
      </div>

      {product.benefits && (
        <div>
          <h3 className="text-lg font-semibold mb-3">Principais Benefícios</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {product.benefits.map((benefit, index) => (
              <div key={index} className="flex items-start gap-2">
                <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
                <span className="text-sm">{benefit}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-muted/30 p-4 rounded-lg">
        <div className="flex items-center gap-2 mb-2">
          <Building2 className="w-5 h-5 text-primary" />
          <span className="font-medium">Adoção no Mercado</span>
        </div>
        <p className="text-sm text-muted-foreground">
          <strong>{product.similarCompaniesCount} empresas</strong> similares à sua já utilizam esta solução,
          com resultados comprovados em eficiência operacional e ROI.
        </p>
      </div>
    </div>
  )

  const renderFeatures = () => (
    <div className="space-y-6">
      {product.keyFeatures && (
        <div>
          <h3 className="text-lg font-semibold mb-4">Funcionalidades Principais</h3>
          <div className="space-y-3">
            {product.keyFeatures.map((feature, index) => (
              <div key={index} className="flex items-start gap-3 p-3 border rounded-lg">
                <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                <span className="text-sm">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {product.technicalSpecs && (
        <div>
          <h3 className="text-lg font-semibold mb-4">Especificações Técnicas</h3>
          <div className="space-y-2">
            {product.technicalSpecs.map((spec, index) => (
              <div key={index} className="flex justify-between py-2 border-b border-border/50">
                <span className="text-sm font-medium">{spec.label}</span>
                <span className="text-sm text-muted-foreground">{spec.value}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )

  const renderSuccessStories = () => (
    <div className="space-y-6">
      {product.successStories?.map((story, index) => (
        <div key={index} className="border rounded-lg p-6 space-y-4">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-muted rounded-full flex items-center justify-center">
                <span className="text-sm font-medium">
                  {story.companyName.substring(0, 2).toUpperCase()}
                </span>
              </div>
              <div>
                <h4 className="font-semibold">{story.companyName}</h4>
                <p className="text-sm text-muted-foreground">{story.industry}</p>
              </div>
            </div>
            <Badge variant="secondary" className="text-xs">
              {story.metric}
            </Badge>
          </div>

          <div className="bg-primary/5 p-4 rounded-lg border-l-4 border-primary">
            <p className="text-sm italic mb-2">"{story.testimonial}"</p>
            <div className="flex items-center gap-2">
              <span className="text-xs font-medium">{story.contactName}</span>
              <span className="text-xs text-muted-foreground">•</span>
              <span className="text-xs text-muted-foreground">{story.contactRole}</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-green-500" />
            <span className="text-sm font-medium text-green-700">{story.result}</span>
          </div>
        </div>
      )) || (
        <div className="text-center py-8">
          <Users className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
          <p className="text-muted-foreground">Casos de sucesso em breve</p>
        </div>
      )}
    </div>
  )

  const renderResources = () => (
    <div className="space-y-4">
      {product.resources?.map((resource, index) => (
        <div
          key={index}
          className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/30 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              {resource.type === 'pdf' && <Download className="w-4 h-4 text-primary" />}
              {resource.type === 'video' && <Play className="w-4 h-4 text-primary" />}
              {resource.type === 'demo' && <Zap className="w-4 h-4 text-primary" />}
            </div>
            <div>
              <h4 className="font-medium text-sm">{resource.title}</h4>
              <p className="text-xs text-muted-foreground">{resource.description}</p>
            </div>
          </div>
          <Button size="sm" variant="outline" onClick={() => handleDownloadMaterial(resource.url)}>
            {resource.type === 'demo' ? 'Acessar' : 'Download'}
          </Button>
        </div>
      )) || (
        <div className="text-center py-8">
          <Download className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
          <p className="text-muted-foreground">Recursos em breve</p>
        </div>
      )}
    </div>
  )

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-background rounded-lg max-w-4xl max-h-[90vh] w-full mx-4 overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex-shrink-0 p-6 border-b">
          <div className="flex items-start gap-4">
            <img
              src={product.image || "/placeholder.svg"}
              alt={product.name}
              className="w-16 h-16 object-cover rounded-lg flex-shrink-0"
            />
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h2 className="text-xl font-bold leading-tight pr-8">{product.name}</h2>
                  <div className="flex items-center gap-2 mt-2">
                    <Badge variant="outline" className="text-xs">
                      {product.category}
                    </Badge>
                    <Badge variant="outline" className="text-xs">
                      {product.segment}
                    </Badge>
                    {product.isCompanyRecommended && (
                      <Badge className="bg-primary text-primary-foreground text-xs">
                        <TrendingUp className="w-3 h-3 mr-1" />
                        Recomendado
                      </Badge>
                    )}
                  </div>
                </div>
                <Button variant="ghost" size="icon" onClick={onClose}>
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs Navigation */}
        <div className="flex-shrink-0 p-4">
          <div className="flex space-x-1 bg-muted p-1 rounded-lg">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === tab.id
                      ? "bg-background text-foreground shadow-sm"
                      : "text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              )
            })}
          </div>
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {activeTab === 'overview' && renderOverview()}
          {activeTab === 'features' && renderFeatures()}
          {activeTab === 'success-stories' && renderSuccessStories()}
          {activeTab === 'resources' && renderResources()}
        </div>

        {/* Footer Actions */}
        <div className="flex-shrink-0 border-t p-6">
          <div className="flex flex-col sm:flex-row gap-3">
            <Button onClick={handleScheduleMeeting} className="flex-1 bg-primary hover:bg-primary/90">
              <Calendar className="w-4 h-4 mr-2" />
              Agendar Reunião
            </Button>
            <Button variant="outline" onClick={handleRequestDemo} className="flex-1 bg-transparent">
              <Play className="w-4 h-4 mr-2" />
              Solicitar Demo
            </Button>
            <div className="flex gap-2">
              <Button size="sm" variant="outline">
                <Phone className="w-4 h-4" />
              </Button>
              <Button size="sm" variant="outline">
                <Mail className="w-4 h-4" />
              </Button>
            </div>
          </div>
          <p className="text-xs text-muted-foreground text-center mt-3">
            Nossa equipe entrará em contato em até 2 horas úteis
          </p>
        </div>
      </div>
    </div>
  )
}
