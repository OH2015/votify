import "./login.css";
import axios from "axios";
import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { API_URL } from "./config";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const RootElement = styled.div`
  max-width: 800px;
  margin: auto;
`;

const Title = styled.div`
  font-weight: bold;
`;

function UpdateHistory() {
  const [updateContents, setUpdateContents] = useState([]);
  const getUpdateContent = () => {
    axios
      .get(`${API_URL}/api/update_content/`, {
        withCredentials: true,
      })
      .then((response) => {
        setUpdateContents(response.data);
      })
      .catch((error) => {
        console.log("エラーが発生しました" + error);
        alert("通信に失敗しました");
      });
  };
  // 初期処理
  useEffect(() => {
    getUpdateContent();
  }, []);

  return (
    <>
      <RootElement>
        <div className="row">
          <div className="col-6 font-weight-bold">内容</div>
          <div className="col-6 font-weight-bold">追加日</div>
        </div>
        {updateContents.map((updateContent) => (
          <div className="row">
            <div className="col-6">{updateContent.content_text}</div>
            <div className="col-6">{updateContent.created_at}</div>
          </div>
        ))}
      </RootElement>
    </>
  );
}

export default UpdateHistory;
