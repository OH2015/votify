import React, {useState,memo} from 'react'
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
    margin-top:50px;
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

// コメントコンポーネント
const Footer = memo(() => {
    // コメント表示/非表示をステートで保持
    const [opend,setOpend] = useState(false);
    // コメント表示/非表示切り替え処理
    const toggleClickHandler = () =>{
        setOpend(true);
    }
    return (
        <div>
            {opend ? (
            <Container className="containner-fluid">
                <CommentForm>
                    <Draft maxLength={1000} />
                    <br/>
                    <CommentButton className="btn btn-primary">コメント</CommentButton>
                </CommentForm>

                <Comment/>
                <Comment/>
            </Container>
            ) : <CommentToggle onClick={toggleClickHandler}>コメントを表示する</CommentToggle>}
        </div>
    )
});

export default Footer;