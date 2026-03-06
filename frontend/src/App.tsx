import { CanvasRoot } from './components/Canvas/CanvasRoot'
import './App.css'

function App() {
  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
      {/* Sidebar — will be added in issue #13 */}
      <CanvasRoot />
    </div>
  )
}

export default App
