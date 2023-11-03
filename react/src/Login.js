import axios from "axios";
import { API_URL, GOOGLE_CLIENT_ID } from "./config";
import styled from "styled-components";
import { Link } from "react-router-dom";
import React, { useEffect, useRef } from "react";
import { GoogleLogin } from "react-google-login";
import { gapi } from "gapi-script";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const Container = styled.div`
  max-width: 400px;
  width: 100%;
`;
const onSuccess = (response) => {
  const email = response.profileObj.email;
  const google_id = response.profileObj.googleId;
  axios
    .post(
      `${API_URL}/api/google_login/`,
      { email: email, google_id: google_id },
      { withCredentials: true }
    )
    .then((response) => {
      if (response.data.result) {
        window.location.href = "/";
      } else {
        window.alert(response.data.message);
      }
    })
    .catch((error) => {
      window.alert("API通信中にエラーが発生しました。");
      console.log("Error Google login", error);
    });
};

const onFailure = (response) => {
  window.alert("ログインに失敗しました。");
  console.log("failure" + response);
};

function Login() {
  const emailRef = useRef(null);
  const passwordRef = useRef(null);

  useEffect(() => {
    function start() {
      gapi.client.init({ clientId: GOOGLE_CLIENT_ID, scope: "" });
    }
    gapi.load("client:auth2", start);
  }, []);

  const doLogin = (event) => {
    event.preventDefault();
    const email = emailRef.current.value;
    const password = passwordRef.current.value;
    axios
      .post(
        `${API_URL}/api/login/`,
        { email: email, password: password },
        { withCredentials: true }
      )
      .then((response) => {
        if (response.data.result) {
          window.location.href = "/";
        } else {
          alert(response.data.message);
        }
      })
      .catch((error) => {
        alert("サーバ内部でエラーが発生しました");
        console.log(error);
      });
  };

  return (
    <>
      <Container className="border rounded mx-auto bg-white">
        <form onSubmit={doLogin}>
          <div className="border-bottom p-3">
            <label>メールアドレス:</label>
            <input type="email" ref={emailRef} required className="w-100" />
          </div>
          <div className="border-bottom p-3">
            <label>パスワード:</label>
            <input
              type="password"
              ref={passwordRef}
              required
              className="w-100"
            />
          </div>
          <div className="border-bottom p-3">
            <button className="btn btn-primary w-100">ログイン</button>
          </div>
        </form>
        <Link
          to="/password_reset_mail"
          className="btn btn-link w-100"
          style={{ textDecoration: "none" }}
        >
          パスワードをお忘れですか？
        </Link>
      </Container>
      <Container className="mx-auto mt-2 p-5">
        <Link
          to="/account_register"
          className="btn btn-secondary w-100 mb-4"
          style={{ textDecoration: "none" }}
        >
          新規登録
        </Link>
        <GoogleLogin
          clientId={GOOGLE_CLIENT_ID}
          buttonText="Googleアカウントでログイン"
          onSuccess={onSuccess}
          onFailure={onFailure}
          cookiePolicy="single_host_origin"
          className="w-100"
        />
      </Container>
    </>
  );
}

export default Login;
