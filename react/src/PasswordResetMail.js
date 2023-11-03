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

function PasswordResetMail() {
  const emailRef = useRef(null);

  const [completed, setCompleted] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (document.forms[0].reportValidity()) {
      axios
        .post(
          API_URL + "/api/password_reset_mail/",
          {
            email: emailRef.current.value,
          },
          {
            withCredentials: true,
          }
        )
        .then((response) => {
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

  return (
    <Container className="border rounded mx-auto bg-white">
      {!completed ? (
        <form onSubmit={handleSubmit}>
          <div className="border-bottom p-3">
            <h4 className="m-0">パスワード再設定のメール発行</h4>
          </div>
          <div className="border-bottom p-3">
            <label>メールアドレス:</label>
            <input
              ref={emailRef}
              type="email"
              required
              className="w-100"
            ></input>
          </div>
          <div className="border-bottom p-3">
            <button className="btn btn-primary">送信</button>
          </div>
        </form>
      ) : (
        <div className="border-bottom p-3">
          メールを送信しました。<br></br>
          パスワードの再設定を完了するには24時間以内に添付したURLにアクセスしてください。
          <br></br>
          <Link to="/">TOPへ戻る</Link>
        </div>
      )}
    </Container>
  );
}

export default PasswordResetMail;
