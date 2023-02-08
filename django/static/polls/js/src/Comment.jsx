import React from 'react'
import styled from 'styled-components'

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
const CommentContainer = styled.div`
    margin-top: 20px;
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
const CommentHeader = styled.div`
    display: flex;
`
const CommentText = styled.p`
    white-space: pre-wrap;
    font-size: 13px;
`
const CommentFooter = styled.div`
`

// コメントコンポーネント
export default Comment = () => {
    return (
        <Container className="containner-fluid">
            <CommentForm>
                <Draft maxLength={1000} />
                <br/>
                <CommentButton className="btn btn-primary">コメント</CommentButton>
            </CommentForm>

            <CommentContainer>
                <CommentHeader>
                    <h5>ユーザ名</h5>
                    <span>　</span>
                    <span>1日前</span>
                </CommentHeader>
                <CommentText>コメントコメントコメントコメント<br/>
                コメントコメントコメントコメントコメント<br/>
                コメントコメントコメントコメントコメント<br/>
                コメントコメントコメントコメントコメント<br/>
                コメントコメントコメントコメントコメント<br/>
                </CommentText>
                <CommentFooter/>
            </CommentContainer>
        </Container>
    )
}