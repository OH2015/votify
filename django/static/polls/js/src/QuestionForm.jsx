import React, { useState, useEffect } from "react";
import styled from "styled-components";


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
`;

const FormButtons = styled.div`
  margin-top: 30px;
`

// ボディコンポーネント
const QuestionForm = ({handleClosePopup}) => {
  const [formData, setFormData] = useState({ 
    title: '',
    explanation: '',
    choices: ['',''],
    genre: 'その他',
    auth_level: 0,
    user: null,
  });

  const handleChange = event => {
    let { name, value} = event.target;
    if(name=="choice"){
      formData.choices[event.target.dataset.index] = value
    }
    setFormData(prevFormData => ({
      ...prevFormData,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    const res = await axios.post("/create_question/",formData);
  };

  return (
    <PopupOverlay onClick={handleClosePopup}>
        <PopupContent onClick={(event) => event.stopPropagation()}>
          <div className="container mt-12">
                <form>
                  <div className="form-group">
                    <label htmlFor="title">タイトル</label>
                    <input value={formData.title}
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
                      rows="3"
                      placeholder="説明を入力してください"
                    ></textarea>
                  </div>
                  <div className="form-group">
                    <label htmlFor="options">選択肢</label>
                    {formData.choices.map((choice,idx) => (<input
                      name="choice"
                      data-index={idx}
                      key={idx}
                      value={choice}
                      onInput={handleChange}
                      className="form-control"
                      placeholder="選択肢を入力してください"
                    />))}
                  </div>
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
                        <button onClick={handleClosePopup}
                          className="btn btn-secondary btn-block"
                        >
                          キャンセル
                        </button>
                      </div>
                    </div>
                  </FormButtons>
                </form>
          </div>
        </PopupContent>
      </PopupOverlay>
  );
};

export default QuestionForm;
