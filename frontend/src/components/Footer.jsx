// Footer 组件 - 参考 Augment Code 的底部设计风格
function Footer() {
    const techStack = [
        {
            name: "FastAPI",
            url: "https://fastapi.tiangolo.com/",
            category: "Backend"
        },
        {
            name: "SQLAlchemy",
            url: "https://www.sqlalchemy.org/",
            category: "Database"
        },
        {
            name: "React",
            url: "https://react.dev/",
            category: "Frontend"
        },
        {
            name: "Vite",
            url: "https://vitejs.dev/",
            category: "Build Tool"
        },
        {
            name: "LangChain",
            url: "https://www.langchain.com/",
            category: "AI Framework"
        },
        {
            name: "OpenAI",
            url: "https://openai.com/",
            category: "AI Service"
        },
        {
            name: "SQLite",
            url: "https://www.sqlite.org/",
            category: "Database"
        }
    ];

    const socialLinks = [
        {
            name: "GitHub",
            url: "https://github.com/RRRuby1225/Generate_Your_ADV_CN",
            icon: "🔗"
        }
    ];

    return (
        <footer className="app-footer">
            <div className="footer-content">
                {/* 技术栈部分 */}
                <div className="footer-section">
                    <h3>技术栈</h3>
                    <div className="tech-links">
                        {techStack.map((tech, index) => (
                            <a
                                key={index}
                                href={tech.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="tech-link"
                                title={`${tech.name} - ${tech.category}`}
                            >
                                {tech.name}
                            </a>
                        ))}
                    </div>
                </div>

                {/* 项目链接部分 */}
                <div className="footer-section">
                    <h3>项目</h3>
                    <div className="project-links">
                        {socialLinks.map((link, index) => (
                            <a
                                key={index}
                                href={link.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="project-link"
                                title={`访问 ${link.name}`}
                            >
                                <span className="link-icon">{link.icon}</span>
                                {link.name}
                            </a>
                        ))}
                    </div>
                </div>

                {/* 项目描述 */}
                <div className="footer-section footer-description">
                    <h3>关于项目</h3>
                    <p>这是一个用于学习全栈开发的 AI 故事生成器项目，展示了现代 Web 开发技术栈的综合应用。</p>
                </div>
            </div>

            {/* 版权信息 */}
            <div className="footer-bottom">
                <p>&copy; 2024 AI 故事生成器. 用于学习目的的开源项目.</p>
            </div>
        </footer>
    );
}

export default Footer;