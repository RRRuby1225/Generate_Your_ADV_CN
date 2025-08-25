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

    return (
        <div className="theme-input-container">
            <h2>创作你的冒险故事</h2>
            <p>为你的互动故事输入一个主题</p>

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
        </div>
    )
}

export default ThemeInput;