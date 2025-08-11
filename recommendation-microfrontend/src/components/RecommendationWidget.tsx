import { ArrowRight, Building2, Calendar, Loader2, TrendingUp, Users } from 'lucide-react'
import { useEffect, useState } from 'react'
import { RecommendationService } from '../services/recommendationService'
import { RecommendationProduct } from '../types/recommendation'
import { ProductDetailModal } from './ProductDetailModal'
import { Badge } from './ui/badge'
import { Button } from './ui/button'
import { Card, CardContent } from './ui/card'

interface RecommendationWidgetProps {
  clientId: string
  title?: string
  subtitle?: string
}

export function RecommendationWidget({
  clientId,
  title = "Produtos Recomendados para Sua Empresa",
  subtitle = "Baseado na análise de empresas similares do seu setor"
}: RecommendationWidgetProps) {
  const [products, setProducts] = useState<RecommendationProduct[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [hoveredProduct, setHoveredProduct] = useState<string | null>(null)
  const [selectedProduct, setSelectedProduct] = useState<RecommendationProduct | null>(null)

  // Função para gerar imagem usando serviços externos confiáveis
  const generateProductImage = (productName: string, index: number): string => {
    console.log(`🖼️ Gerando imagem para "${productName}" (index ${index}):`);
    
    // Usar picsum.photos com seed baseado no nome para consistência
    const seed = productName.toLowerCase().replace(/[^a-z0-9]/g, '') + index;
    const imageUrl = `https://picsum.photos/400/300?random=${seed}`;
    
    console.log(`   URL gerada: ${imageUrl}`);
    return imageUrl;
  };

  // Função para gerar fallback usando dummyimage.com
  const generateFallbackImage = (productName: string, index: number): string => {
    const colors = ['4f46e5', '3b82f6', '10b981', 'f59e0b', 'ef4444'];
    const bgColor = colors[index % colors.length];
    
    const words = productName.split(/[\s-]+/);
    const initials = words.slice(0, 2).map(word => word.charAt(0).toUpperCase()).join('');
    
    const fallbackUrl = `https://www.dummyimage.com/400x300/${bgColor}/ffffff?text=${encodeURIComponent(initials)}`;
    
    console.log(`🔄 Fallback para "${productName}": ${fallbackUrl}`);
    return fallbackUrl;
  };

  // Estado para controlar fallbacks de imagem
  const [imageErrors, setImageErrors] = useState<Set<string>>(new Set());

  // Função para lidar com erros de imagem
  const handleImageError = (productId: string, productName: string, index: number, event: React.SyntheticEvent<HTMLImageElement>) => {
    console.log(`❌ Erro ao carregar imagem para "${productName}"`);
    
    if (!imageErrors.has(productId)) {
      // Primeira tentativa de fallback
      setImageErrors(prev => new Set(prev).add(productId));
      const fallbackUrl = generateFallbackImage(productName, index);
      (event.target as HTMLImageElement).src = fallbackUrl;
    } else {
      // Se o fallback também falhou, usar CSS avatar
      console.log(`⚠️ Fallback também falhou, usando CSS avatar`);
      (event.target as HTMLImageElement).style.display = 'none';
      // O CSS avatar será mostrado via conditional rendering
    }
  };

  useEffect(() => {
    loadRecommendations()
  }, [clientId])

  const loadRecommendations = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await RecommendationService.getRecommendations(clientId, 3) // Reduzido para 3 recomendações
      
      // Transformar dados da API para o formato esperado pelo componente
      const transformedProducts: RecommendationProduct[] = response.recommendations.map((rec: any, index) => ({
        id: rec.id || `product-${index}`,
        name: rec.product_name || rec.name || 'Produto Sem Nome',
        description: rec.description || `${rec.reason || 'Solução recomendada com base em análise de empresas similares'}. Score de confiança: ${((rec.confidence || 0) * 100).toFixed(1)}%`,
        score: rec.confidence || rec.score || 0,
        category: rec.category || 'Categoria não informada',
        segment: rec.segment || 'Segmento não informado',
        isCompanyRecommended: index === 0, // Primeiro produto é sempre recomendado
        similarCompaniesCount: Math.floor(Math.random() * 50) + 10, // Mock temporário
        benefits: [
          'Redução de custos operacionais',
          'Aumento de produtividade',
          'Integração com sistemas existentes'
        ], // Mock temporário
        image: '', // Não vamos usar mais imagem externa
        detailedDescription: `${rec.description} Esta solução foi desenvolvida especificamente para empresas do seu segmento, oferecendo integração completa com sistemas existentes e suporte especializado 24/7.`,
        keyFeatures: [
          'Dashboard executivo com métricas em tempo real',
          'Integração nativa com principais ERPs do mercado', 
          'Relatórios customizáveis e automáticos',
          'API robusta para integrações personalizadas',
          'Suporte técnico especializado 24/7'
        ],
        technicalSpecs: [
          { label: 'Tempo de implementação', value: '2-4 semanas' },
          { label: 'Integrações disponíveis', value: '50+ sistemas' },
          { label: 'Uptime garantido', value: '99.9%' },
          { label: 'Suporte técnico', value: '24/7 em português' }
        ],
        successStories: [
          {
            companyName: 'TechCorp Solutions',
            industry: 'Tecnologia',
            result: 'Redução de 45% no tempo de processamento',
            metric: 'ROI: 280%',
            testimonial: 'A implementação superou nossas expectativas. Em 3 meses já víamos resultados significativos na produtividade da equipe.',
            contactName: 'Carlos Silva',
            contactRole: 'CTO'
          }
        ],
        resources: [
          {
            type: 'pdf',
            title: 'Guia Completo da Solução',
            description: 'Documento técnico com todas as funcionalidades',
            url: '/resources/guia-completo.pdf'
          }
        ]
      }))
      
      setProducts(transformedProducts)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar recomendações')
    } finally {
      setLoading(false)
    }
  }

  const handleScheduleMeeting = (productName: string) => {
    console.log(`Agendando reunião para produto: ${productName}`)
    // Integração futura com sistema de agendamento
  }

  const handleViewDetails = (product: RecommendationProduct) => {
    setSelectedProduct(product)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <span className="ml-2 text-muted-foreground">Carregando recomendações...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="mb-4 text-red-500">
          Erro ao carregar recomendações: {error}
        </div>
        <Button onClick={loadRecommendations} variant="outline">
          Tentar Novamente
        </Button>
      </div>
    )
  }

  if (products.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mb-4 text-muted-foreground">
          Nenhuma recomendação encontrada para este cliente.
        </div>
      </div>
    )
  }

  return (
    <section className="py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-start gap-3 mb-4">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Users className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-foreground mb-2">{title}</h2>
              <p className="text-muted-foreground text-base max-w-2xl">
                {subtitle}. Encontradas {products.length} soluções personalizadas para o cliente {clientId}.
              </p>
            </div>
          </div>
        </div>

        {/* Products Grid */}
        <div className={`grid gap-6 ${
          products.length === 3
            ? "grid-cols-1 md:grid-cols-3"
            : products.length === 4
              ? "grid-cols-1 md:grid-cols-2 lg:grid-cols-4" 
              : "grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
        }`}>
          {products.map((product) => (
            <Card
              key={product.id}
              className="group hover:shadow-xl transition-all duration-300 border-border relative overflow-hidden"
              onMouseEnter={() => setHoveredProduct(product.id)}
              onMouseLeave={() => setHoveredProduct(null)}
            >
              <CardContent className="p-0">
                {/* Imagem do produto com fallback */}
                <div className="relative overflow-hidden">
                  {(() => {
                    const productIndex = products.indexOf(product);
                    const hasImageError = imageErrors.has(product.id);
                    
                    if (hasImageError) {
                      // Mostrar avatar CSS se a imagem falhou
                      const colors = [
                        { bg: 'bg-indigo-500', text: 'text-white' },
                        { bg: 'bg-blue-500', text: 'text-white' },
                        { bg: 'bg-emerald-500', text: 'text-white' },
                        { bg: 'bg-amber-500', text: 'text-white' },
                        { bg: 'bg-red-500', text: 'text-white' }
                      ];
                      
                      const colorScheme = colors[productIndex % colors.length];
                      const words = product.name.split(' ').filter(word => word.length > 0);
                      const initials = words.length >= 2 
                        ? `${words[0][0]}${words[1][0]}`.toUpperCase()
                        : `${words[0][0]}${words[0][1] || 'X'}`.toUpperCase();
                      
                      return (
                        <div
                          className={`
                            w-full h-48 flex items-center justify-center text-6xl font-bold
                            ${colorScheme.bg} ${colorScheme.text}
                            transition-transform group-hover:scale-105 duration-300
                          `}
                        >
                          {initials}
                        </div>
                      );
                    } else {
                      // Mostrar imagem externa
                      return (
                        <img
                          src={generateProductImage(product.name, productIndex)}
                          alt={product.name}
                          className="w-full h-48 object-cover transition-transform group-hover:scale-105 duration-300"
                          onError={(e) => handleImageError(product.id, product.name, productIndex, e)}
                          loading="lazy"
                        />
                      );
                    }
                  })()}

                  {/* Company Recommendation Badge */}
                  {product.isCompanyRecommended && (
                    <div className="absolute top-4 left-4">
                      <Badge className="bg-primary text-primary-foreground text-xs font-medium">
                        <TrendingUp className="w-3 h-3 mr-1" />
                        Recomendado
                      </Badge>
                    </div>
                  )}

                  {/* Score Badge */}
                  <div className="absolute top-4 right-4">
                    <Badge variant="secondary" className="text-xs">
                      Score: {(product.score * 100).toFixed(1)}%
                    </Badge>
                  </div>

                  {/* Hover Overlay with CTA */}
                  <div
                    className={`absolute inset-0 bg-black/60 flex items-center justify-center transition-opacity duration-300 ${
                      hoveredProduct === product.id ? "opacity-100" : "opacity-0"
                    }`}
                  >
                    <Button
                      onClick={() => handleScheduleMeeting(product.name)}
                      className="bg-primary hover:bg-primary/90 text-primary-foreground"
                    >
                      <Calendar className="w-4 h-4 mr-2" />
                      Agendar Reunião
                    </Button>
                  </div>
                </div>

                {/* Content */}
                <div className="p-6 space-y-4">
                  {/* Category */}
                  <div className="flex items-center gap-2">
                    <div className="text-xs text-muted-foreground font-medium uppercase tracking-wide">
                      {product.category}
                    </div>
                    <div className="w-1 h-1 bg-muted-foreground rounded-full"></div>
                    <div className="text-xs text-muted-foreground">{product.segment}</div>
                  </div>

                  {/* Product Name */}
                  <h3 className="font-semibold text-lg leading-tight group-hover:text-primary transition-colors">
                    {product.name}
                  </h3>

                  {/* Description */}
                  <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3">
                    {product.description}
                  </p>

                  {/* Similar Companies Indicator */}
                  <div className="flex items-center gap-2 pt-2">
                    <div className="flex items-center gap-1">
                      <Building2 className="w-4 h-4 text-muted-foreground" />
                      <span className="text-sm text-muted-foreground">
                        {product.similarCompaniesCount} empresas similares já utilizam
                      </span>
                    </div>
                  </div>

                  {/* Benefits Preview */}
                  {product.benefits && product.benefits.length > 0 && (
                    <div className="pt-2">
                      <div className="flex flex-wrap gap-1">
                        {product.benefits.slice(0, 2).map((benefit, index) => (
                          <Badge key={index} variant="secondary" className="text-xs">
                            {benefit}
                          </Badge>
                        ))}
                        {product.benefits.length > 2 && (
                          <Badge variant="secondary" className="text-xs">
                            +{product.benefits.length - 2} mais
                          </Badge>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Learn More Link */}
                  <Button
                    variant="link"
                    className="p-0 h-auto text-primary hover:text-primary/80 text-sm"
                    onClick={() => handleViewDetails(product)}
                  >
                    Saiba mais sobre este produto
                    <ArrowRight className="w-3 h-3 ml-1" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Footer CTA */}
        <div className="text-center mt-8 p-6 bg-muted/30 rounded-lg">
          <p className="text-sm text-muted-foreground mb-4">
            Quer uma análise personalizada das soluções ideais para sua empresa?
          </p>
          <Button variant="outline" size="lg" className="bg-background">
            <Calendar className="w-4 h-4 mr-2" />
            Falar com Consultor Especializado
          </Button>
        </div>

        {/* Product Detail Modal */}
        {selectedProduct && (
          <ProductDetailModal
            isOpen={!!selectedProduct}
            onClose={() => setSelectedProduct(null)}
            product={selectedProduct}
          />
        )}
      </div>
    </section>
  )
}
