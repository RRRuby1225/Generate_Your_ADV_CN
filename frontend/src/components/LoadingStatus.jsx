/**
 * LoadingStatus组件 - 显示故事生成过程中的加载状态
 * 作用：当用户提交故事主题后，显示一个友好的加载界面，包含：
    * 动态显示正在生成的故事主题
    * 旋转的加载动画（spinner）
    * 用户等待提示信息
 * 这是一个纯展示组件，没有复杂的状态管理，只接收theme参数并显示。
 * @param {string} theme - 用户输入的故事主题
 * @returns {JSX.Element} 加载状态的UI组件
 */

function LoadingStatus({theme}) {
  return (
    <div className="loading-container">
      {/* 显示正在生成的故事主题 */}
      <h2>Generating Your {theme} Story</h2>

      {/* 加载动画容器 */}
      <div className="loading-animation">
          {/* 旋转的加载指示器 */}
          <div className="spinner"></div>
      </div>

      {/* 用户提示信息 */}
      <p className="loading-info">
          Please wait while we generate your story...
      </p>
    </div>
  )
}

export default LoadingStatus;