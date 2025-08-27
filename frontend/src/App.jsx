
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import StoryGenerator from './components/StoryGenerator.jsx'
import StoryLoader from './components/StoryLoader.jsx'
import Footer from './components/Footer.jsx' // 导入 Footer 组件

function App() {
  return (
    <Router>
      {/* 添加包装器，使用 flexbox 布局 */}
      <div className="app-wrapper">
        {/* 主内容区域 */}
        <div className='app-container'>
          <header>
          <h1>AI 故事生成器</h1>
          </header>
          <main>
            <Routes>
              <Route path={"/story/:id"} element={<StoryLoader />} />
              <Route path={"/"} element={<StoryGenerator />} />
            </Routes>
          </main>
        </div>
        {/* Footer 固定在底部 */}
        <Footer />
      </div>
    </Router>
  )
}

export default App
