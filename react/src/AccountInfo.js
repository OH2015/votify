import React, { useEffect, useState, useRef } from "react";
import { Link } from "react-router-dom";
import { PopupContent, PopupOverlay } from "./Common";
import styled from "styled-components";
import axios from "axios";
import { API_URL } from "./config";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const Container = styled.div`
  max-width: 400px;
`;

function AccountInfo() {
  const inputRef = useRef(null);

  const [showPopup, setShowPopup] = useState(false);
  const [user, setUser] = useState({
    username: "ロード中...",
    email: "ロード中...",
    profile: "ロード中...",
    auth_provider: "",
  });

  const getUserInfo = () => {
    axios
      .get(`${API_URL}/api/get_user_info/`, { withCredentials: true })
      .then((response) => {
        if (!response.data.result) {
          window.location.href = "/login";
        } else {
          setUser({
            ...user,
            ...response.data.user,
          });
        }
      });
  };

  const handleOpenPopup = () => {
    setShowPopup(true);
  };

  const handleClosePopup = () => {
    setShowPopup(false);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const value = inputRef.current.value;
    axios
      .post(
        `${API_URL}/api/update_username/`,
        { username: value },
        { withCredentials: true }
      )
      .then((response) => {
        window.alert(response.data.message);
        if (response.data.result) {
          handleClosePopup();
          window.location.reload();
        }
      });
  };

  useEffect(() => {
    getUserInfo();
  }, []);

  return (
    <>
      {showPopup ? (
        <PopupOverlay onClick={handleClosePopup}>
          <PopupContent onClick={(event) => event.stopPropagation()}>
            <form onSubmit={handleSubmit}>
              <label>新しいユーザ名：</label>
              <br></br>
              <input
                autoFocus={true}
                defaultValue={user.username}
                className="w-100"
                ref={inputRef}
                required
                minLength={2}
                maxLength={30}
              ></input>
              <div>
                <button className="btn btn-primary mt-3 w-100">更新</button>
              </div>
            </form>
          </PopupContent>
        </PopupOverlay>
      ) : null}
      <Container className="border rounded mx-auto">
        <div className="border-bottom p-3 m-0 row">
          <div className="col-9">
            <label>ユーザ名:</label>
            <p className="m-0">{user.username}</p>
          </div>
          <div className="col-3">
            <button
              className="btn btn-sm btn-outline-secondary w-100"
              onClick={handleOpenPopup}
            >
              編集
            </button>
          </div>
        </div>
        <div className="border-bottom p-3 m-0 row">
          <div className="col-9">
            <label>メールアドレス:</label>
            <p className="m-0">{user.email}</p>
          </div>
          <div className="col-3"></div>
        </div>
        <div className="p-3 row m-0">
          <div className="col-9">
            <label>パスワード:</label>
            <p className="m-0">********</p>
          </div>
          <div className="col-3">
            {user.auth_provider === "email" ? (
              <Link
                to="/password_change"
                className="btn btn-sm btn-outline-secondary w-100"
              >
                編集
              </Link>
            ) : null}
          </div>
        </div>
      </Container>
    </>
  );
}

export default AccountInfo;
