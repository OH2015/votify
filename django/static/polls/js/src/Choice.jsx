import React,{memo} from 'react'
import styled from 'styled-components'

const ProgressBar = styled.div`
    position: absolute;
    display: inline-flex;
    background-color: #6495ED;
    width: ${props => props.progress}%;
    height:100%;
    border-radius: 5px;
`
const PercentageArea = styled.div`
    position: absolute;
    display: inline-flex;
    background-color: lightgray;
    width: 100%;
    height: 100%;
    border-radius: 5px;
`
const ChoiceText = styled.div`
    display: inline-flex;
    z-index: 1;
    margin-left:5px;
`
const PercentText = styled.div`
    display: inline-flex;
    z-index: 1;
    margin-right:5px;
    margin-left: auto
`

const ChoiceBox = styled.div`
    width: 90%;
    height:50px;
    display: flex;
    position: relative;
    margin: 5px;
    border-radius: 5px;
    align-items: center;
    border:${prop => prop.voted ? '3px solid #98FB98' : 'none'};
    color:${prop => prop.voted ? '#98FB98' : 'black'};
    &:hover{
        cursor: pointer;
    }
`
// チョイスコンポーネント
const Choice = memo(({id,choice_text,vote_id,progress}) => {
    return (
        <ChoiceBox key={id} voted={vote_id} >
            <ChoiceText>{choice_text} </ChoiceText>
            <PercentText>{Math.floor(progress)}%</PercentText>
            <PercentageArea/>
            <ProgressBar progress={progress}/>
        </ChoiceBox>
    );
});

export default Choice;
