import React, { useCallback, useState, useRef, useEffect } from "react";
import styled from "styled-components";
import axios from "axios";
import { API_URL } from "../config";

const QuestionContainer = styled.div`
  background-color: #f5f5f5;
  margin-bottom: 20px;
  width: 100%;
  border: gray 1px solid;
  border-radius: 5px;
  padding: 5px;
  box-shadow: 3px 3px 3px;
`;
const QuestionTitle = styled.h3`
  text-align: left;
`;
const Explanation = styled.div`
  text-align: left;
  white-space: pre-wrap;
`;
const CopyText = styled.input`
  position: absolute;
  left: -9999px;
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
const CommentForm = styled.div`
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
const CommentText = styled.p`
  white-space: pre-wrap;
  font-size: 15px;
  text-align: left;
`;

// 投稿コンポーネント
const Post = ({ p_question, setIsLoading, userId }) => {
  // 選択肢のリストをステートとして保持
  const [question, setQuestion] = useState(p_question);
  const [opend, setOpend] = useState(false); // コメント表示/非表示
  const inputRef = useRef(null);
  const ref = useRef(null);

  // URL取得
  const urlText = `${window.location.host}/?question_id=${question.id}`;

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
        getQuestion();
      })
      .catch((e) => {
        alert("API通信中にエラーが発生しました。");
      });

    setIsLoading(false);
  };

  const getQuestion = () => {
    axios
      .get(`${API_URL}/api/question/?question_id=${question.id}`, {
        withCredentials: true,
      })
      .then((response) => {
        setQuestion(response.data[0]);
      })
      .catch((e) => {
        alert("API通信中にエラーが発生しました。");
      });
  };

  // 得票率を計算して返却
  const getProgress = useCallback(
    (votes) => {
      const sum = question.choices.reduce(
        (sum, choice) => sum + choice.votes,
        0
      );
      return (sum ? votes / sum : 0) * 100;
    },
    [question.choices]
  );

  // クリップボードにリンクをコピーする処理
  const copyUrl = () => {
    inputRef.current.select();
    document.execCommand("Copy");
  };

  // コメント表示/非表示切り替え処理
  const toggleClickHandler = () => {
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
  const handleCommentDelete = (id) => {
    if (window.confirm("このコメントを削除してもよろしいですか？")) {
      axios
        .delete(`${API_URL}/api/comment/${id}/`, {
          withCredentials: true,
        })
        .then((response) => {
          getQuestion();
        });
    }
  };

  // コメント入力欄の大きさ制御
  const autoResize = () => {
    const draft = ref.current;
    draft.style.height = "28px";
    draft.style.height = `${draft.scrollHeight}px`;
  };

  // コメント投稿処理
  const handleSubmitComment = () => {
    const draft = ref.current;
    if (!userId) {
      alert("コメントするにはログインが必要です");
      return;
    }
    if (draft.value === "") return;

    axios
      .post(
        `${API_URL}/api/comment/`,
        {
          question: question.id,
          text: draft.value,
          user_id: userId,
        },
        { withCredentials: true }
      )
      .then((response) => {
        draft.value = "";
        autoResize();
        getQuestion();
        setOpend(true);
      })
      .catch((e) => {
        alert("API通信中にエラーが発生しました。");
      });
  };

  return (
    <QuestionContainer>
      <div
        style={{ display: "flex", justifyContent: "space-between" }}
        className="text-start"
      >
        {question.author.username}
        <CopyText ref={inputRef} value={urlText} readOnly />
        <i
          style={{ cursor: "pointer" }}
          class="fa-solid fa-lg fa-ellipsis m-2"
          data-bs-toggle="dropdown"
        ></i>
        <ul class="dropdown-menu dropdown-menu-end">
          <li>
            <button class="dropdown-item" onClick={copyUrl}>
              URLをコピー
            </button>
          </li>
          {userId === question.author.id && (
            <li>
              <button class="dropdown-item" onClick={deleteClickHandler}>
                削除
              </button>
            </li>
          )}
        </ul>
      </div>
      <div>
        <QuestionTitle>{question.title}</QuestionTitle>
      </div>
      <Explanation>{question.explanation}</Explanation>
      {question.choices.map((choice) => (
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
      ))}
      <div style={{ textAlign: "left" }}>{question.votes}票</div>
      <div
        style={{ cursor: "pointer", textAlign: "left" }}
        onClick={toggleClickHandler}
      >
        <i class="fa-solid fa-comment mx-1"></i>
        {question.comments.length}
      </div>

      {opend && (
        <>
          <CommentForm>
            <Draft maxLength={1000} ref={ref} onInput={autoResize} />
            <button
              className="btn btn-primary"
              onClick={handleSubmitComment}
            >
              送信
            </button>
          </CommentForm>
          {question.comments.map((comment) => (
            <div className="mt-2">
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <div>
                  <span className="fw-bold">{comment.user.username}</span>
                  <span className="mx-4">{comment.disp_date}</span>
                </div>
                {userId === comment.user.id && (
                  <div>
                    <i
                      style={{ cursor: "pointer" }}
                      class="fa-solid fa-lg fa-ellipsis m-2"
                      data-bs-toggle="dropdown"
                    ></i>
                    <ul class="dropdown-menu  dropdown-menu-end">
                      <li>
                        <button
                          class="dropdown-item"
                          onClick={() => handleCommentDelete(comment.id)}
                        >
                          削除
                        </button>
                      </li>
                    </ul>
                  </div>
                )}
              </div>
              <CommentText>{comment.text}</CommentText>
            </div>
          ))}
        </>
      )}
    </QuestionContainer>
  );
};

export default Post;
