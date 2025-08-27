import {useState} from "react"

function ThemeInput({onSubmit}) {
    const [theme, setTheme]= useState("");
    const [error, setError] = useState("")

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!theme.trim()) {
            setError("请输入故事主题");
            return
        }

        onSubmit(theme);
    }

    // 添加示例主题点击功能
    const handleExampleClick = (exampleTheme) => {
        setTheme(exampleTheme);
        setError(""); // 清除错误信息
    }

    return (
        <div className="theme-input-container">
            <h2>创作你的冒险故事</h2>
            <p>为你的互动故事输入一个主题，AI将为你生成独特的分支剧情</p>

            <form onSubmit={handleSubmit}>
                <div className="input-group">
                    <input
                        type="text"
                        value={theme}
                        onChange={(e) => setTheme(e.target.value)}
                        placeholder="输入故事主题（例如：海盗、太空、中世纪...）"
                        className={error ? 'error' : ''}
                    />
                    {error && <p className="error-text">{error}</p>}
                </div>
                <button type="submit" className='generate-btn'>
                    生成故事
                </button>
            </form>

            {/* 添加示例主题标签 */}
            <div className="examples">
                <h3>热门主题：</h3>
                <ul>
                    <li onClick={() => handleExampleClick("神秘的古堡探险")}>神秘的古堡探险</li>
                    <li onClick={() => handleExampleClick("太空站危机")}>太空站危机</li>
                    <li onClick={() => handleExampleClick("魔法学院")}>魔法学院</li>
                    <li onClick={() => handleExampleClick("海盗寻宝")}>海盗寻宝</li>
                    <li onClick={() => handleExampleClick("赛博朋克都市")}>赛博朋克都市</li>
                    <li onClick={() => handleExampleClick("末日求生")}>末日求生</li>
                </ul>
            </div>
        </div>
    )
}

export default ThemeInput;