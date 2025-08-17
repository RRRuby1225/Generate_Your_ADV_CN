import {useState} from "react"

/**
 * ThemeInput组件 - 故事主题输入表单
 * 提供用户输入故事主题的界面，包含：
    * 文本输入框
    * 表单验证（检查是否为空）
    * 提交按钮
    * 错误信息显示
 * 
 * @param {Function} onSubmit - 提交主题时的回调函数
 * @returns {JSX.Element} 主题输入表单组件
 */


function ThemeInput({onSubmit}) {
    // 状态管理：存储用户输入的主题
    const [theme, setTheme]= useState("");
    // 状态管理：存储表单验证错误信息
    const [error, setError] = useState("")

    /**
     * 处理表单提交
     * 验证输入并调用onSubmit回调
     * 
     * @param {Event} e - 表单提交事件对象
     */
    const handleSubmit = (e) => {
        e.preventDefault(); // 阻止默认的表单提交行为

        // 验证主题是否为空或只包含空格
        if (!theme.trim()) {
            setError("Please enter a theme name");
            return
        }

        // 调用父组件传入的提交函数
        onSubmit(theme);
    }

    return (
        <div className="theme-input-container">
            {/* 页面标题 */}
            <h2>Generate Your Adventure</h2>
            {/* 说明文字 */}
            <p>Enter a theme for your interactive story</p>

            {/* 主题输入表单 */}
            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    {/* 主题输入框 */}
                    <input
                        type="text"
                        value={theme} // 受控组件：值由state控制
                        onChange={(e) => setTheme(e.target.value)} // 更新state
                        placeholder="Enter a theme (e.g. prirates, space, medieval...)"
                        className={error ? 'error' : ''} // 根据错误状态动态设置样式
                    />
                    {/* 错误信息显示 */}
                    {error && <p className="error-text">{error}</p>}
                </div>
                {/* 提交按钮 */}
                <button type="submit" className='generate-btn'>
                    Generate Story
                </button>
            </form>
        </div>
    )
}

export default ThemeInput;