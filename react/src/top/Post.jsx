import React, { useCallback, useState, useRef, useEffect } from "react";
import styled from "styled-components";
import Comment from "./Comment";
import axios from "axios";
import { API_URL } from "../config";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const QuestionContainer = styled.div`
  background-color: #f5f5f5;
  margin-bottom: 20px;
  width: 100%;
  border: gray 1px solid;
  border-radius: 5px;
  padding: 5px;
  box-shadow: 3px 3px 3px;
`;
const QuestionHeader = styled.div`
  display: flex;
  justify-content: space-between;
`;
const QuestionTitle = styled.h3`
  text-align: left;
`;
const Explanation = styled.div`
  text-align: left;
`;
const CopyText = styled.input`
  position: absolute;
  left: -9999px;
`;

const CopyButton = styled.button`
  border: none;
  background-color: transparent;
  cursor: pointer;
  font-size: 15px;
  text-align: right;
`;
const ProgressBar = styled.div`
  position: absolute;
  display: inline-flex;
  background-color: #6495ed;
  width: ${(props) => props.progress}%;
  height: 100%;
  border-radius: 5px;
`;
const PercentageArea = styled.div`
  position: absolute;
  display: inline-flex;
  background-color: lightgray;
  width: 100%;
  height: 100%;
  border-radius: 5px;
`;
const ChoiceText = styled.div`
  display: inline-flex;
  z-index: 1;
  margin-left: 5px;
`;
const PercentText = styled.div`
  display: inline-flex;
  z-index: 1;
  margin-right: 5px;
  margin-left: auto;
`;

const ChoiceBox = styled.div`
  width: 90%;
  height: 50px;
  display: flex;
  position: relative;
  margin: 5px;
  border-radius: 5px;
  align-items: center;
  border: ${(prop) => (prop.voted ? "3px solid #98FB98" : "none")};
  color: ${(prop) => (prop.voted ? "#98FB98" : "black")};
  &:hover {
    cursor: pointer;
  }
`;
const CommentToggle = styled.button`
  border: none;
  background-color: transparent;
  cursor: pointer;
  font-size: 15px;
  &:hover {
    cursor: pointer;
  }
`;
const CommentForm = styled.div`
  padding-bottom: 10px;
  padding-top: 10px;
  border-bottom: solid gray 1px;
  display: flex;
  align-items: center;
`;
const Draft = styled.textarea`
  width: calc(100% - 150px);
  height: 28px;
  resize: none;
  overflow: hidden;
  margin-right: 30px;
`;
const CommentButton = styled.button`
  width: 100px;
`;

// 投稿コンポーネント
const Post = ({ question, setIsLoading, userId }) => {
  // 選択肢のリストをステートとして保持
  const [choices, setChoices] = useState(question.choices);
  const [copied, setCopied] = useState(false);
  const [opend, setOpend] = useState(false); // コメント表示/非表示
  const [comments, setComments] = useState(question.comments); // コメントのリスト
  const inputRef = useRef(null);
  const ref = useRef(null);

  // URL取得
  const urlText = `${window.location.hostname}/?question_id=${question.id}`;

  // 初期処理
  useEffect(() => {}, []);

  // 選択肢が押下された時の処理
  const choiceClickHandler = (choice) => {
    setIsLoading(true);
    axios
      .post(
        `${API_URL}/api/vote/`,
        {
          question: question.id,
          choice: choice.id,
        },
        { withCredentials: true }
      )
      .then((response) => {
        getChoices();
      })
      .catch((e) => {
        alert("API通信中にエラーが発生しました。");
      });

    setIsLoading(false);
  };

  const getComments = async () => {
    // コメント取得
    const result = await axios.get(
      `${API_URL}/api/comment/?question_id=${question.id}`,
      { withCredentials: true }
    );
    setComments(result.data);
  };

  const getChoices = () => {
    axios
      .get(`${API_URL}/api/choice/?question_id=${question.id}`, {
        withCredentials: true,
      })
      .then((response) => {
        setChoices(response.data);
      })
      .catch((e) => {
        alert("API通信中にエラーが発生しました。");
      });
  };

  // 得票率を計算して返却
  const getProgress = useCallback((votes) => {
    const sum = choices.reduce((sum, choice) => sum + choice.votes, 0);
    return (sum ? votes / sum : 0) * 100;
  }, [choices]);

  // クリップボードにリンクをコピーする処理
  const copyUrl = () => {
    inputRef.current.select();
    document.execCommand("Copy");
    setCopied(true);
    setTimeout(() => {
      setCopied(false);
    }, 1000);
  };

  // コメント表示/非表示切り替え処理
  const toggleClickHandler = () => {
    if (!opend && !comments.length) {
      getComments();
    }
    setOpend(!opend);
  };
  // 投稿削除処理
  const deleteClickHandler = async () => {
    if (window.confirm("この投稿を削除してもよろしいですか？")) {
      await axios.delete(`${API_URL}/api/question/${question.id}/`, {
        withCredentials: true,
      });
      window.location.href = "/";
    }
  };
  // コメント削除処理
  const handleCommentDelete = (deletedCommentId) => {
    setComments(
      comments.filter((comment) => comment.id !== deletedCommentId)
    );
  };
  // コメント入力欄の大きさ制御
  const autoResize = () => {
    const draft = ref.current;
    draft.style.height = "28px";
    draft.style.height = `${draft.scrollHeight}px`;
  };
  // コメント投稿処理
  const submit_comment = async () => {
    const draft = ref.current;
    if (userId === 0) {
      alert("コメントするにはログインが必要です");
      return;
    }
    if (draft.value === "") return;

    // コメントをPOST送信
    const result = await axios.post(
      `${API_URL}/api/comment/`,
      {
        question: question.id,
        text: draft.value,
        user_id: userId,
      },
      { withCredentials: true }
    );
    draft.value = "";
    autoResize();

    setComments(comments.concat(result.data));
    setOpend(true);
  };

  return (
    <QuestionContainer>
      <div className="text-start">{question.author.username}</div>
      <QuestionHeader>
        <QuestionTitle>{question.title}</QuestionTitle>
        <CopyText ref={inputRef} value={urlText} readOnly />
        <CopyButton onClick={copyUrl}>
          <i className="fas fa-copy"></i>
          {copied ? "Copied!" : "Copy URL"}
        </CopyButton>
      </QuestionHeader>
      <Explanation>{question.explanation}</Explanation>
      {choices.map((choice) => {
        return (
          <ChoiceBox
            key={choice.id}
            voted={choice.voted}
            onClick={() => choiceClickHandler(choice)}
          >
            <ChoiceText>{choice.choice_text}</ChoiceText>
            <PercentText>{Math.floor(getProgress(choice.votes))}%</PercentText>
            <PercentageArea />
            <ProgressBar progress={getProgress(choice.votes)} />
          </ChoiceBox>
        );
      })}

      <CommentToggle onClick={toggleClickHandler}>
        コメント({comments.length})
      </CommentToggle>
      {userId === question.author.id && (
        <CommentToggle onClick={deleteClickHandler}>削除</CommentToggle>
      )}

      {opend && (
        <>
          <CommentForm>
            <Draft maxLength={1000} ref={ref} onInput={autoResize} />
            <CommentButton className="btn btn-primary" onClick={submit_comment}>
              送信
            </CommentButton>
          </CommentForm>
          {comments.map((comment) => (
            <Comment
              key={comment.id}
              {...comment}
              userId={userId}
              onDelete={handleCommentDelete}
            />
          ))}
        </>
      )}
    </QuestionContainer>
  );
};

export default Post;
