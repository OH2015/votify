import React,{useState, useEffect} from 'react'
import styled from 'styled-components'
import Post from './Post'

const RootElement = styled.div`
    max-width: 800px;
    margin: auto;
`

// ボディコンポーネント
const Body = () => {
    const [posts,setPosts] = useState([]); //投稿一覧
    
    // 初期処理
    useEffect(() => {
        const getQuestions = async () => {
          const res = await axios.get('/api/questions/');
          setPosts(res.data);
        }
        getQuestions();
    }, []);

    return (
        <RootElement>
            {posts.map(post => (<Post key={post.id} {...post}/>))}
        </RootElement>
    );
}

export default Body;
