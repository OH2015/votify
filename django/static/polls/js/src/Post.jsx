import React,{useCallback, useState} from 'react'
import styled from 'styled-components'
import Choice from './Choice'
import Footer from './Footer'

const QuestionContainer = styled.div`
    margin-bottom: 20px;
    width: 100%;
    border: gray 1px solid;
    border-radius: 5px;
    padding: 5px;
    box-shadow: 3px 3px 3px;
`

const QuestionTitle = styled.h3`
`
const Explanation = styled.div`
`

// 投稿コンポーネント
const Post = ({id,title,explanation,choices: ini_choices,comments}) => {
    // 選択肢のリストをステートとして保持
    const [choices, setChoices] = useState(ini_choices);

    // 選択肢が押下された時の処理
    const choiceClickHandler = async (choice_id) => {
        // 選択された選択肢
        const choice = choices.find(e=>e.id == choice_id);
        // 投票済みの選択肢
        const posted = choices.find(e=>e.vote_id);

        // 選択済みなら解除
        if(choice.vote_id){
            await axios.delete(`/api/vote/${choice.vote_id}/`)
            choice.vote_id = null // vote_idをリセット
            choice.votes -= 1 // 得票数-1
        }else{
            // 投票先にPOST
            const res = await axios.post('/api/vote/',{
                "question": id,
                "choice": choice_id,
                "user": null
            },)
            // 帰ってきたvote_idをセット
            choice.vote_id = res.data.id;
            choice.votes += 1; // 得票数+1
            
            // 既に選択済みのPOSTをDELETE
            if(posted){   
                await axios.delete(`/api/vote/${posted.vote_id}/`)
                posted.vote_id = null // vote_idをリセット
                posted.votes -= 1 // 得票数-1
            }
        }
        
        // 選択肢のリストを上書き
        setChoices([...choices]);
    };

    // 得票率を計算して返却
    const getProgress = useCallback(votes => {
        const sum = choices.reduce((sum,el) => sum + el.votes,0)
        return (sum ? votes / sum : 0) * 100;
    },[]);

    return (
        <QuestionContainer>
            <QuestionTitle>{title}</QuestionTitle>
            <Explanation>{explanation}</Explanation>
            {choices.map((choice) => {
                return (
                    <div key={choice.id} onClick={() => choiceClickHandler(choice.id)}>
                        <Choice {...choice} progress={getProgress(choice.votes)}/>
                    </div>
                )
            })}
            <Footer questionId={id}/>
        </QuestionContainer>
    )
}

export default Post;