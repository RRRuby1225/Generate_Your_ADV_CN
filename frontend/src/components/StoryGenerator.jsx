import {useState, useEffect} from "react"
import {useNavigate} from "react-router-dom";
import axios from "axios";
import ThemeInput from "./ThemeInput.jsx";
import LoadingStatus from "./LoadingStatus.jsx";
import {API_BASE_URL} from "../util.js";

/**
 * StoryGenerator组件 - 故事生成的主要控制器
 * 作用：这是整个应用的核心组件，负责：
    * 接收用户输入的主题
    * 向后台API发送故事生成请求
    * 管理异步任务的执行状态
    * 轮询任务进度
    * 处理成功/失败结果
    * 导航到故事页面
 * 
 * @returns {JSX.Element} 故事生成器组件
 */
function StoryGenerator() {
    const navigate = useNavigate() // React Router导航钩子
    
    // 状态管理：存储用户输入的主题
    const [theme, setTheme] = useState("")
    // 状态管理：存储后台任务的ID
    const [jobId, setJobId] = useState(null)
    // 状态管理：存储任务的当前状态
    const [jobStatus, setJobStatus] = useState(null)
    // 状态管理：存储错误信息
    const [error, setError] = useState(null)
    // 状态管理：控制加载状态显示
    const [loading, setLoading] = useState(false)

    /**
     * 副作用：设置任务状态轮询
     * 当有正在处理的任务时，每5秒检查一次状态
     */
    useEffect(() => {
        let pollInterval; // 轮询定时器引用

        // 只有当任务存在且状态为"processing"时才启动轮询
        if (jobId && jobStatus === "processing") {
            pollInterval = setInterval(() => {
                pollJobStatus(jobId)
            }, 5000) // 每5秒轮询一次
        }

        // 清理函数：组件卸载或依赖变化时清除定时器
        return () => {
            if (pollInterval) {
                clearInterval(pollInterval)
            }
        }
    }, [jobId, jobStatus]) // 依赖数组：当jobId或jobStatus变化时重新执行

    /**
     * 创建故事生成任务
     * 向后台API发送请求，创建异步任务
     * 
     * @param {string} theme - 故事主题
     */
    const generateStory = async (theme) => {
        setLoading(true) // 开始加载
        setError(null) // 清除之前的错误
        setTheme(theme) // 保存主题

        try {
            // 发送POST请求创建故事生成任务
            const response = await axios.post(`${API_BASE_URL}/stories/create`, {theme})
            const {job_id, status} = response.data
            
            // 保存任务信息
            setJobId(job_id)
            setJobStatus(status)

            // 立即检查一次任务状态
            pollJobStatus(job_id)
        } catch (e) {
            setLoading(false) // 停止加载
            setError(`Failed to generate story: ${e.message}`) // 设置错误信息
        }
    }

    /**
     * 轮询任务状态
     * 定期检查后台任务的执行状态
     * 
     * @param {string} id - 任务ID
     */
    const pollJobStatus = async (id) => {
        try {
            // 获取任务状态
            const response = await axios.get(`${API_BASE_URL}/jobs/${id}`)
            const {status, story_id, error: jobError} = response.data
            setJobStatus(status)

            // 任务完成且有故事ID
            if (status === "completed" && story_id) {
                fetchStory(story_id)
            } 
            // 任务失败
            else if (status === "failed" || jobError) {
                setError(jobError || "Failed to generate story")
                setLoading(false)
            }
        } catch (e) {
            // 忽略404错误（任务可能还在创建中）
            if (e.response?.status !== 404) {
                setError(`Failed to check story status: ${e.message}`)
                setLoading(false)
            }
        }
    }

    /**
     * 获取生成完成的故事
     * 任务完成后，导航到故事页面
     * 
     * @param {string} id - 故事ID
     */
    const fetchStory = async (id) => {
        try {
            setLoading(false) // 停止加载
            setJobStatus("completed") // 设置任务状态为完成
            navigate(`/story/${id}`) // 导航到故事页面
        } catch (e) {
            setError(`Failed to load story: ${e.message}`)
            setLoading(false)
        }
    }

    /**
     * 重置组件状态
     * 清除所有状态，回到初始状态
     */
    const reset = () => {
        setJobId(null)
        setJobStatus(null)
        setError(null)
        setTheme("")
        setLoading(false)
    }

    return (
        <div className="story-generator">
            {/* 错误信息显示 */}
            {error && (
                <div className="error-message">
                    <p>{error}</p>
                    <button onClick={reset}>Try Again</button>
                </div>
            )}

            {/* 主题输入表单 - 只在没有任务且无错误且未加载时显示 */}
            {!jobId && !error && !loading && <ThemeInput onSubmit={generateStory}/>}

            {/* 加载状态显示 - 在生成过程中显示 */}
            {loading && <LoadingStatus theme={theme} />}
        </div>
    )
}

export default StoryGenerator