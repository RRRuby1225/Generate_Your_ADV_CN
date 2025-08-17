import {useState, useEffect} from 'react';
import {useParams, useNavigate} from "react-router-dom"
import axios from 'axios';
import LoadingStatus from "./LoadingStatus.jsx";
import StoryGame from "./StoryGame.jsx";
import {API_BASE_URL} from "../util.js";

/**
 * StoryLoader组件 - 故事加载和显示控制器
 * 作用：负责从URL参数获取故事ID并加载故事数据，包含：
    * 从路由参数获取故事ID
    * 调用API加载故事数据
    * 处理加载状态和错误
    * 条件渲染不同的UI组件
 * 
 * @returns {JSX.Element} 故事加载器组件
 */




function StoryLoader() {
    const {id} = useParams(); // 从URL路径获取故事ID参数
    const navigate = useNavigate(); // React Router导航钩子
    
    // 状态管理：存储加载的故事数据
    const [story, setStory] = useState(null);
    // 状态管理：控制加载状态显示
    const [loading, setLoading] = useState(true)
    // 状态管理：存储错误信息
    const [error, setError] = useState(null);

    /**
     * 副作用：组件挂载时加载故事
     * 当组件首次渲染或故事ID变化时执行
     */
    useEffect(() => {
        loadStory(id)
    }, [id]) // 依赖数组：当id变化时重新加载故事

    /**
     * 从API加载故事数据
     * 根据故事ID获取完整的故事信息
     * 
     * @param {string} storyId - 故事的唯一标识符
     */
    const loadStory = async (storyId) => {
        setLoading(true) // 开始加载
        setError(null) // 清除之前的错误

        try {
            // 发送GET请求获取故事数据
            const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`)
            setStory(response.data) // 保存故事数据
            setLoading(false) // 停止加载
        } catch (err) {
            // 处理404错误：故事不存在
            if (err.response?.status === 404) {
                setError("Story is not found.")
            } 
            // 处理其他错误
            else {
                setError("Failed to load story")
            }
        } finally {
            setLoading(false) // 确保加载状态被重置
        }
    }

    /**
     * 创建新故事
     * 导航回故事生成器页面
     */
    const createNewStory = () => {
        navigate("/") // 导航到根路径（故事生成器）
    }

    // 条件渲染：显示加载状态
    if (loading) {
        return <LoadingStatus theme={"story"} />
    }

    // 条件渲染：显示错误信息
    if (error) {
        return (
            <div className="story-loader">
                <div className="error-message">
                    <h2>Story Not Found</h2>
                    <p>{error}</p>
                    <button onClick={createNewStory}>Go to Story Generator</button>
                </div>
            </div>
        )
    }

    // 条件渲染：显示故事游戏界面
    if (story) {
        return (
            <div className="story-loader">
                <StoryGame story={story} onNewStory={createNewStory} />
            </div>
        )
    }
}

export default StoryLoader;