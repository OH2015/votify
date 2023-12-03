import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { API_URL } from "./config";

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
    let value = event.target.value;
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

  const onDelteClicked = (idx) => {
    if (jsonData.choices.length < 3) {
      window.alert("選択肢は2つ以上必要です。");
      return;
    }
    setJsonData((prevjsonData) => ({
      ...prevjsonData,
      choices: [
        ...prevjsonData.choices.slice(0, idx),
        ...prevjsonData.choices.slice(idx + 1),
      ],
    }));
  };

  const handleSubmit = (event) => {
    // デフォルトのsubmit処理キャンセル
    event.preventDefault();
    // API送信
    axios
      .post(API_URL + "/api/create_question/", jsonData, {
        withCredentials: true,
      })
      .then((response) => {
        window.location.href = "/";
      })
      .catch((e) => {
        window.alert("API通信中にエラーが発生しました。");
      });
  };

  return (
    <>
      {logined ? (
        <form onSubmit={handleSubmit}>
          <div
            className="border rounded container m-auto"
            style={{ maxWidth: "500px" }}
          >
            <div className="my-3">
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
            <div className="my-3">
              <label htmlFor="description">説明</label>
              <textarea
                value={jsonData.explanation}
                onInput={onExplanationChange}
                name="explanation"
                className="form-control"
                placeholder="説明を入力してください"
              ></textarea>
            </div>
            <div className="my-3">
              <label htmlFor="options">選択肢</label>
              <div
                className="mx-3 btn btn-sm btn-outline-secondary"
                onClick={(event) => onPlusClicked(event)}
              >
                <i className="fa-solid fa-plus"></i>
              </div>
              {jsonData.choices.map((choice, idx) => (
                <div className="input-group">
                  <input
                    required
                    name="choice"
                    data-index={idx}
                    key={idx}
                    value={choice}
                    onInput={onChoiceChange}
                    className="form-control my-1"
                    placeholder="選択肢を入力してください"
                  />
                  <div
                    className="m-auto btn"
                    onClick={() => onDelteClicked(idx)}
                  >
                    <i class="fa-solid fa-trash"></i>
                  </div>
                </div>
              ))}
            </div>
            <div
              className="my-3"
              style={{ display: "flex" }}
            >
              <button className="btn btn-primary btn-block">作成</button>
              <Link
                to="/"
                className="btn btn-secondary btn-block mx-3"
                style={{ textDecoration: "none" }}
              >
                キャンセル
              </Link>
            </div>
          </div>
        </form>
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
