import React,{useState} from 'react'
import styled from 'styled-components'
import Comment from './Comment'

const QuestionContainer = styled.div`
    width: 100%;
    border: gray 1px solid;
    border-radius: 5px;
    padding: 5px;
    box-shadow: 3px 3px 3px;
`
const ProgressBar = styled.div`
    position: absolute;
    display: inline-flex;
    background-color: rgb(193, 235, 77);
    width: 50%;
    height: 50px;
    border-radius: 5px;
`
const PercentageArea = styled.div`
    position: absolute;
    display: inline-flex;
    background-color: rgba(151, 143, 143, 0.655);
    width: 100%;
    height: 100%;
    border-radius: 5px;
`

const ChoiceText = styled.div`
    display: inline-flex;
    z-index: 1;
`

const ChoiceBox = styled.div`
    width: 90%;
    height:50px;
    display: flex;
    position: relative;
    margin: 5px;
    border-radius: 5px;
    align-items: center;
    &:hover{
        cursor: pointer;
    }
`

const CommentToggle = styled.div`
    &:hover{
        cursor: pointer;
    }
`


// 投稿コンポーネント
const Post = ({post}) => {
    const [opend,setOpend] = useState(false);

    const choiceClickHandler = () => {
        console.log("click!")
    }

    const toggleClickHandler = () =>{
        setOpend(true);
    }

    return (
        <QuestionContainer>
            <h3>{post.title}</h3>
            <div>
                {post.explanation}
            </div>
            <div>
                {post.choices.map(choice => {
                    return (
                        <ChoiceBox key={choice.id} onClick={choiceClickHandler}>
                            <ChoiceText>{choice.choice_text}</ChoiceText>
                            <PercentageArea/>
                            <ProgressBar/>
                        </ChoiceBox>
                    )
                })}
            </div>
            <div>
                {!opend && <CommentToggle onClick={toggleClickHandler}>コメントを表示する</CommentToggle>}
                {opend && <Comment/>}
            </div>
        </QuestionContainer>
    )
}

export default Post;