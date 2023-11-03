import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { RoundButton, PlusIcon } from "./top/Top";
import axios from "axios";
import { API_URL } from "./config";

const MinusIcon = styled.span`
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: auto;
  width: 10px;
  height: 10px;
  &::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    margin: auto;
    width: 2px;
    height: 10px;
    background-color: white;
  }
  &::before {
    transform: rotate(90deg);
  }
`;

const FlexBox = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 15px;

  > button {
    margin: 0 5px;
  }
`;

const Button = styled.button`
  width: 120px;
`;

// ボディコンポーネント
const QuestionCreate = ({ handleClosePopup }) => {
  const [logined, setLogined] = useState(true);
  const [jsonData, setJsonData] = useState({
    title: "",
    explanation: "",
    choices: ["", ""],
    genre: "その他",
    auth_level: 0,
  });

  // 初期処理
  useEffect(() => {
    axios
      .get(`${API_URL}/api/get_user_info/`, {
        withCredentials: true,
      })
      .then((response) => {
        if (!response.data.result) {
          setLogined(false);
        }
      })
      .catch((error) => {
        alert("API通信に失敗しました");
      });
  }, []);

  const onTitleChange = (event) => {
    let { name, value } = event.target;
    setJsonData((prevjsonData) => ({ ...prevjsonData, [name]: value }));
  };

  const onExplanationChange = (event) => {
    let { name, value } = event.target;
    setJsonData((prevjsonData) => ({ ...prevjsonData, [name]: value }));
  };

  const onChoiceChange = (event) => {
    let { name, value } = event.target;
    setJsonData((prevjsonData) => ({
      ...prevjsonData,
      choices: prevjsonData.choices.map((choice, index) =>
        index === parseInt(event.target.dataset.index) ? value : choice
      ),
    }));
  };

  const onPlusClicked = (event) => {
    setJsonData((prevjsonData) => ({
      ...prevjsonData,
      choices: [...prevjsonData.choices, ""],
    }));
  };

  const onMinusClicked = (event) => {
    setJsonData((prevjsonData) => ({
      ...prevjsonData,
      choices: prevjsonData.choices.slice(0, -1),
    }));
  };

  const handleSubmit = () => {
    // 入力値チェック
    const filledChoices = jsonData.choices.filter((choice) => choice);
    if (!jsonData.title) {
      window.alert("タイトルは空にできません");
      return;
    }
    if (filledChoices.length < 2) {
      window.alert("選択肢は最低2つ必要です");
      return;
    }
    jsonData.choices = filledChoices;
    // API送信
    axios
      .post(API_URL + "/api/create_question/", jsonData, {
        withCredentials: true,
      })
      .then((res) => {
        window.location.href = "/";
      })
      .catch((e) => {
        window.alert("投稿に失敗しました。");
      });
  };

  return (
    <>
      {logined ? (
        <div className="container m-auto" style={{ maxWidth: "500px" }}>
          <div className="form-group">
            <label htmlFor="title">タイトル</label>
            <input
              required
              value={jsonData.title}
              onInput={onTitleChange}
              name="title"
              className="form-control"
              placeholder="タイトルを入力してください"
            />
          </div>
          <div className="form-group">
            <label htmlFor="description">説明欄</label>
            <textarea
              value={jsonData.explanation}
              onInput={onExplanationChange}
              name="explanation"
              className="form-control"
              placeholder="説明を入力してください"
            ></textarea>
          </div>
          <div className="form-group">
            <label htmlFor="options">選択肢</label>
            {jsonData.choices.map((choice, idx) => (
              <input
                required
                name="choice"
                data-index={idx}
                key={idx}
                value={choice}
                onInput={onChoiceChange}
                className="form-control"
                placeholder="選択肢を入力してください"
              />
            ))}
          </div>
          <FlexBox>
            <RoundButton onClick={(event) => onPlusClicked(event)}>
              <PlusIcon></PlusIcon>
            </RoundButton>
            {jsonData.choices.length > 2 && (
              <RoundButton onClick={(event) => onMinusClicked(event)}>
                <MinusIcon></MinusIcon>
              </RoundButton>
            )}
          </FlexBox>
          <FlexBox>
            <Button
              onClick={handleSubmit}
              className="btn btn-primary btn-block"
            >
              作成
            </Button>
            <Button
              onClick={handleClosePopup}
              className="btn btn-secondary btn-block"
            >
              キャンセル
            </Button>
          </FlexBox>
        </div>
      ) : (
        <div>
          投稿するにはログインを行ってください。
          <Link to="/login">
            <button className="btn btn-secondary">ログイン</button>
          </Link>
        </div>
      )}
    </>
  );
};

export default QuestionCreate;
