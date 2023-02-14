import React from 'react'
import styled from 'styled-components'


const CommentContainer = styled.div`
    margin-top: 20px;
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
export default Comment = ({id, user, text}) => {
    return (
        <CommentContainer>
            <CommentHeader>
                <h5>{user.username}</h5>
                <span>　</span>
                <span>1日前</span>
            </CommentHeader>
            <CommentText>{text}
            </CommentText>
            <CommentFooter/>
        </CommentContainer>
    )
}