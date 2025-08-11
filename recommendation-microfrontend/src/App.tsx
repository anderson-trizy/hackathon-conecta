import { RecommendationWidget } from './components/RecommendationWidget'
import './index.css'

function App() {
  // Pegar clientId da URL ou usar default para desenvolvimento
  const urlParams = new URLSearchParams(window.location.search)
  const clientId = urlParams.get('clientId') || '400'

  return (
    <div className="min-h-screen bg-background">
      <RecommendationWidget 
        clientId={clientId}
        title="Soluções Recomendadas"
        subtitle="Baseado no perfil da sua empresa e análise de mercado"
      />
    </div>
  )
}

export default App
