import React, {useState,memo, useEffect} from 'react'
import styled from 'styled-components'
import Comment from './Comment'

const CommentToggle = styled.div`
    &:hover{
        cursor: pointer;
    }
`
const Container = styled.div`
    border-top: solid gray 1px;
    width: 100%;
    margin-top:30px;
`
const CommentForm = styled.div`
    padding-bottom: 10px;
    padding-top: 10px;
    border-bottom: solid gray 1px;
    display: flex;
    align-items: center;
`
const Draft = styled.textarea`
    width:calc(100% - 150px);
    height:28px;
    resize:none;
    overflow: hidden;
    margin-right: 30px;
`
const CommentButton = styled.button`
    width: 100px;
`

// フッターコンポーネント
const Footer = memo(({questionId}) => {
    const [opend, setOpend] = useState(false);// コメント表示/非表示
    const [comment, setComment] = useState('');// 入力中のコメント
    const [commentList, setCommentList] = useState([]);// コメントのリスト

    // 初期処理
    useEffect(() => {
        const getCommentList = async() => {
            // コメント取得
            const result = await axios.get(`/api/comment/?question_id=${questionId}`);
            setCommentList(result.data);
        }
        getCommentList()
    },[]);

    // コメント表示/非表示切り替え処理
    const toggleClickHandler = () => {setOpend(true)};

    // コメント入力時処理
    const inputHandler = element => {
        // コメント入力欄の大きさ制御
        element.target.style.height = "5px";
        element.target.style.height = `${element.target.scrollHeight}px`;
        // コメントステートを更新
        setComment(element.target.value);
    }
    // コメント投稿処理
    const submit_comment = async () => {
        const user_id = document.getElementById('hidden_user_id').value;

        // コメントをPOST送信
        const result = await axios.post('/api/comment/',{
            "question": questionId,
            "text": comment,
            "user_id": parseInt(user_id),
        },)
        // 入力欄を初期化
        setComment('');
        // コメントのリストを追加
        commentList.push(result.data)
        setCommentList(commentList)
    }

    return (
        <div>
            {(opend || commentList.length == 0) ? (
            <Container className="containner-fluid">
                <CommentForm>
                    <Draft maxLength={1000} onInput={inputHandler} value={comment}/>
                    <br/>
                    <CommentButton className="btn btn-primary" onClick={submit_comment}>コメント</CommentButton>
                </CommentForm>

                {commentList.map(comment => (
                    <Comment key={comment.id} {...comment}/>
                ))}
            </Container>
            ) : <CommentToggle onClick={toggleClickHandler}>コメントを表示する</CommentToggle>}
        </div>
    )
});

export default Footer;