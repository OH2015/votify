import React, {useState,memo, useEffect, useRef} from 'react'
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
    const ref = useRef(null);
    const [opend, setOpend] = useState(false);// コメント表示/非表示
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
    const toggleClickHandler = () => {setOpend(!opend)};

    // コメント入力欄の大きさ制御
    const autoResize = () => {
        const draft = ref.current;
        draft.style.height = "28px";
        draft.style.height = `${draft.scrollHeight}px`;
    }
    // コメント入力欄削除
    const deleteDraft = () => {
        const draft = ref.current;
        draft.value = ''
    }
    // コメント投稿処理
    const submit_comment = async () => {
        const draft = ref.current;
        const user_id = document.getElementById('hidden_user_id').value;
        if (user_id == 'None'){
            window.alert("コメントするにはログインが必要です")
            return;
        }

        // コメントをPOST送信
        const result = await axios.post('/api/comment/',{
            "question": questionId,
            "text": draft.value,
            "user_id": parseInt(user_id),
        },)
        deleteDraft()
        autoResize()
        
        setCommentList(commentList.concat(result.data));
        setOpend(true);
    }

    return (
        <div>
            {(opend || commentList.length == 0) ? (
            <Container className="containner-fluid">
                <CommentForm>
                    <Draft maxLength={1000} ref={ref} onInput={autoResize}/>
                    <br/>
                    <CommentButton className="btn btn-primary" onClick={submit_comment}>コメント</CommentButton>
                </CommentForm>

                {commentList.map(comment => (
                    <Comment key={comment.id} {...comment}/>
                ))}
                <CommentToggle onClick={toggleClickHandler}>コメントを非表示にする</CommentToggle>
            </Container>
            
            ) : <CommentToggle onClick={toggleClickHandler}>コメントを表示する</CommentToggle>}
        </div>
    )
});

export default Footer;