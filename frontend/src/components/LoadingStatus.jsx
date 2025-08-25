function LoadingStatus({theme}) {
  return (
    <div className="loading-container">
      <h2>正在生成{theme}故事</h2>

      <div className="loading-animation">
          <div className="spinner"></div>
      </div>

      <p className="loading-info">
          请稍等，我们正在为你创作故事...
      </p>
    </div>
  )
}

export default LoadingStatus;