import {useState, useEffect} from 'react';
import {useParams, useNavigate} from "react-router-dom"
import axios from 'axios';
import LoadingStatus from "./LoadingStatus.jsx";
import StoryGame from "./StoryGame.jsx";
import {API_BASE_URL} from "../util.js";

function StoryLoader() {
    const {id} = useParams();
    const navigate = useNavigate();
    
    const [story, setStory] = useState(null);
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null);

    useEffect(() => {
        loadStory(id)
    }, [id])

    const loadStory = async (storyId) => {
        setLoading(true)
        setError(null)

        try {
            const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`)
            setStory(response.data)
            setLoading(false)
        } catch (err) {
            if (err.response?.status === 404) {
                setError("故事未找到")
            } 
            else {
                setError("加载故事失败")
            }
        } finally {
            setLoading(false)
        }
    }

    const createNewStory = () => {
        navigate("/")
    }

    if (loading) {
        return <LoadingStatus theme={"故事"} />
    }

    if (error) {
        return (
            <div className="story-loader">
                {/* 添加导航栏 */}
                <div className="story-nav">
                    <button onClick={createNewStory} className="home-btn">
                        ← 返回首页
                    </button>
                </div>
                <div className="error-message">
                    <h2>故事未找到</h2>
                    <p>{error}</p>
                    <button onClick={createNewStory}>前往故事生成器</button>
                </div>
            </div>
        )
    }

    if (story) {
        return (
            <div className="story-loader">
                {/* 添加导航栏 */}
                <div className="story-nav">
                    <button onClick={createNewStory} className="home-btn">
                        ← 返回首页
                    </button>
                </div>
                <StoryGame story={story} onNewStory={createNewStory} />
            </div>
        )
    }
}

export default StoryLoader;