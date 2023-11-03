import React, { useRef, useState } from "react";
import styled from "styled-components";
import axios from "axios";
import { API_URL } from "./config";
import { Link } from "react-router-dom";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const Container = styled.div`
  max-width: 400px;
  width: 100%;
`;

function PasswordReset() {
  const oldPasswordRef = useRef(null);
  const newPasswordRef = useRef(null);
  const [masking, setMasking] = useState([true, true]);
  const [message, setMessage] = useState("");
  const [completed, setCompleted] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    if (document.forms[0].reportValidity()) {
      axios
        .post(
          API_URL + "/api/update_password/",
          {
            old_password: oldPasswordRef.current.value,
            new_password: newPasswordRef.current.value,
          },
          {
            withCredentials: true,
          }
        )
        .then((response) => {
          setMessage(response.data.message);
          if (response.data.result) {
            setCompleted(true);
          } else {
            window.alert(response.data.message);
          }
        })
        .catch((error) => {
          console.log("エラーが発生しました" + error);
          alert("通信に失敗しました");
        });
    }
  };

  const toggleMasking = (i) => {
    let newMasking = [...masking];
    newMasking[i] = !newMasking[i];
    setMasking(newMasking);
  };

  return (
    <Container className="border rounded mx-auto bg-white">
      {!completed ? (
        <form onSubmit={handleSubmit}>
          <div className="border-bottom p-3">
            <h4 className="m-0">新しいパスワードを設定</h4>
          </div>
          <div className="border-bottom p-3">
            <label>現在のパスワード:</label>
            <i
              className={masking[0] ? "far fa-eye-slash" : "far fa-eye"}
              onClick={() => toggleMasking(0)}
            ></i>
            <input
              type={masking[0] ? "password" : "text"}
              ref={oldPasswordRef}
              required
              className="w-100"
            />
          </div>
          <div className="border-bottom p-3">
            <label>新しいパスワード:</label>
            <i
              className={masking[1] ? "far fa-eye-slash" : "far fa-eye"}
              onClick={() => toggleMasking(1)}
            ></i>
            <input
              type={masking[1] ? "password" : "text"}
              ref={newPasswordRef}
              required
              className="w-100"
            />
          </div>
          <div className="border-bottom p-3">
            <button className="btn btn-primary">送信</button>
          </div>
        </form>
      ) : (
        <div className="border-bottom p-3">
          {message}
          <br></br>
          <Link to="/login">ログイン画面へ</Link>
        </div>
      )}
    </Container>
  );
}

export default PasswordReset;
