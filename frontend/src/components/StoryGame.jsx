import {useState, useEffect} from 'react';

/**
 * StoryGame组件 - 交互式故事游戏界面
 * 作用：提供完整的游戏体验，包含：
    * 显示故事内容
    * 处理用户选择
    * 管理故事节点导航
    * 显示结局信息
    * 提供重新开始和新故事功能
 * 
 * @param {Object} story - 故事数据对象
 * @param {Function} onNewStory - 创建新故事的回调函数
 * @returns {JSX.Element} 故事游戏组件
 */
function StoryGame({story, onNewStory}) {
    // 状态管理：当前故事节点的ID
    const [currentNodeId, setCurrentNodeId] = useState(null);
    // 状态管理：当前故事节点的完整数据
    const [currentNode, setCurrentNode] = useState(null)
    // 状态管理：当前节点可选择的选项列表
    const [options, setOptions] = useState([])
    // 状态管理：当前节点是否为故事结局
    const [isEnding, setIsEnding] = useState(false)
    // 状态管理：当前节点是否为胜利结局
    const [isWinningEnding, setIsWinningEnding] = useState(false)

    /**
     * 副作用：初始化故事根节点
     * 当故事数据加载完成后，设置起始节点
     */
    useEffect(() => {
        if (story && story.root_node) {
            const rootNodeId = story.root_node.id
            setCurrentNodeId(rootNodeId) // 设置根节点ID
        }
    }, [story]) // 依赖数组：当story变化时重新设置根节点

    /**
     * 副作用：更新当前节点状态
     * 当当前节点ID或故事数据变化时，更新节点信息和选项
     */
    useEffect(() => {
        if (currentNodeId && story && story.all_nodes) {
            // 从故事的所有节点中获取当前节点
            const node = story.all_nodes[currentNodeId]

            // 更新当前节点数据
            setCurrentNode(node)
            // 更新结局状态
            setIsEnding(node.is_ending)
            setIsWinningEnding(node.is_winning_ending)

            // 如果不是结局且有选项，则显示选项列表
            if (!node.is_ending && node.options && node.options.length > 0) {
                setOptions(node.options)
            } else {
                setOptions([]) // 清空选项
            }
        }
    }, [currentNodeId, story]) // 依赖数组：当currentNodeId或story变化时重新执行

    /**
     * 处理用户选择选项
     * 更新当前节点ID，触发节点切换
     * 
     * @param {string} optionId - 用户选择的选项对应的节点ID
     */
    const chooseOption = (optionId) => {
        setCurrentNodeId(optionId) // 切换到新的节点
    }

    /**
     * 重新开始故事
     * 重置到故事的根节点
     */
    const restartStory = () => {
        if (story && story.root_node) {
            setCurrentNodeId(story.root_node.id) // 回到根节点
        }
    }

    return (
        <div className="story-game">
            {/* 故事标题头部 */}
            <header className="story-header">
                <h2>{story.title}</h2>
            </header>

            {/* 故事主要内容区域 */}
            <div className="story-content">
                {/* 当前故事节点内容 */}
                {currentNode && (
                    <div className="story-node">
                        {/* 故事文本内容 */}
                        <p>{currentNode.content}</p>

                        {/* 条件渲染：根据是否为结局显示不同内容 */}
                        {isEnding ? (
                            // 故事结局显示
                            <div className="story-ending">
                                <h3>{isWinningEnding ? "Congratulations" : "The End"}</h3>
                                {isWinningEnding ? "You reached a winning ending" : "Your adventure has ended."}
                            </div>
                        ) : (
                            // 故事选项选择
                            <div className="story-options">
                                <h3>What will you do?</h3>
                                <div className="options-list">
                                    {/* 渲染所有可选择的选项 */}
                                    {options.map((option, index) => {
                                        return (
                                            <button
                                                key={index}
                                                onClick={() => chooseOption(option.node_id)}
                                                className="option-btn"
                                            >
                                                {option.text}
                                            </button>
                                        )
                                    })}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* 故事控制按钮 */}
                <div className="story-controls">
                    <button onClick={restartStory} className="reset-btn">
                        Restart Story
                    </button>
                </div>

                {/* 创建新故事按钮（如果提供了回调函数） */}
                {onNewStory && (
                    <button onClick={onNewStory} className="new-story-btn">
                        New Story
                    </button>
                )}
            </div>
        </div>
    )
}

export default StoryGame