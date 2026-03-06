import { CanvasRoot } from './components/Canvas/CanvasRoot'
import { TerrainForm } from './components/Sidebar/TerrainForm'
import './App.css'

function App() {
  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
      <aside style={{
        width: 280,
        minWidth: 280,
        borderRight: '1px solid #e0e0e0',
        overflowY: 'auto',
        background: '#fff',
      }}>
        <TerrainForm />
      </aside>
      <CanvasRoot />
    </div>
  )
}

export default App
