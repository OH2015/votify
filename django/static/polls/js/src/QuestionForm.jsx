import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { RoundButton, PlusIcon } from "./Body";

const PopupOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  background-color: rgba(0, 0, 0, 0.5);
`;

const PopupContent = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  width: 450px;
  transform: translate(-50%, -50%);
  z-index: 3;
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  max-height: 500px; /* 高さが400pxを超えた場合にスクロールさせる */
  overflow-y: auto; /* 縦方向にスクロールバーを表示する */
`;

const FormButtons = styled.div`
  margin-top: 20px;
`;

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

// ボディコンポーネント
const QuestionForm = ({ handleClosePopup }) => {
  const [formData, setFormData] = useState({
    title: "",
    explanation: "",
    choices: ["", ""],
    genre: "その他",
    auth_level: 0,
    user: null,
  });

  const handleChange = (event, param) => {
    let { name, value } = event.target;
    if (name === "choice") {
      setFormData((prevFormData) => ({
        ...prevFormData,
        choices: prevFormData.choices.map((choice, index) =>
          index === parseInt(event.target.dataset.index) ? value : choice
        ),
      }));
    } else if (param === "plus") {
      setFormData((prevFormData) => ({
        ...prevFormData,
        choices: [...prevFormData.choices, ""],
      }));
    } else if (param === "minus") {
      setFormData((prevFormData) => ({
        ...prevFormData,
        choices: prevFormData.choices.slice(0, -1),
      }));
    } else {
      setFormData((prevFormData) => ({ ...prevFormData, [name]: value }));
    }
  };

  const handleSubmit = async () => {
    // 入力値チェック
    const filledChoices = formData.choices.filter((choice) => choice);
    if (!formData.title) {
      window.alert("タイトルは空にできません");
      return;
    }
    if (filledChoices.length < 2) {
      window.alert("選択肢は最低2つ必要です");
      return;
    }
    formData.choices = filledChoices;
    const res = await axios.post("/create_question/", formData);
    location.href = "/";
  };

  return (
    <PopupOverlay onClick={handleClosePopup}>
      <PopupContent onClick={(event) => event.stopPropagation()}>
        <div className="container mt-12">
          <div className="form-group">
            <label htmlFor="title">タイトル</label>
            <input
              required
              value={formData.title}
              onInput={handleChange}
              name="title"
              className="form-control"
              placeholder="タイトルを入力してください"
            />
          </div>
          <div className="form-group">
            <label htmlFor="description">説明欄</label>
            <textarea
              value={formData.explanation}
              onInput={handleChange}
              name="explanation"
              className="form-control"
              placeholder="説明を入力してください"
            ></textarea>
          </div>
          <div className="form-group">
            <label htmlFor="options">選択肢</label>
            {formData.choices.map((choice, idx) => (
              <input
                required
                name="choice"
                data-index={idx}
                key={idx}
                value={choice}
                onInput={handleChange}
                className="form-control"
                placeholder="選択肢を入力してください"
              />
            ))}
          </div>
          <FormButtons className="form-group">
            <div className="row">
              <div className="col-sm-6">
                <RoundButton onClick={(event) => handleChange(event, "plus")}>
                  <PlusIcon></PlusIcon>
                </RoundButton>
              </div>
              <div className="col-sm-6">
                {formData.choices.length > 2 && (
                  <RoundButton
                    onClick={(event) => handleChange(event, "minus")}
                  >
                    <MinusIcon></MinusIcon>
                  </RoundButton>
                )}
              </div>
            </div>
          </FormButtons>
          <FormButtons className="form-group">
            <div className="row">
              <div className="col-sm-6">
                <button
                  onClick={handleSubmit}
                  className="btn btn-primary btn-block"
                >
                  作成
                </button>
              </div>
              <div className="col-sm-6">
                <button
                  onClick={handleClosePopup}
                  className="btn btn-secondary btn-block"
                >
                  キャンセル
                </button>
              </div>
            </div>
          </FormButtons>
        </div>
      </PopupContent>
    </PopupOverlay>
  );
};

export default QuestionForm;
