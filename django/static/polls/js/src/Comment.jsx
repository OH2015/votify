import React from "react";
import styled from "styled-components";

const CommentContainer = styled.div`
  margin-top: 20px;
`;
const CommentHeader = styled.div`
  display: flex;
`;
const CommentDeleteButton = styled.button`
  border: none;
  background-color: transparent;
  cursor: pointer;
  font-size: 15px;
  &:hover {
    cursor: pointer;
  }
`;
const CommentText = styled.p`
  white-space: pre-wrap;
  font-size: 15px;
  text-align: left;
`;
const CommentFooter = styled.div``;

// コメントコンポーネント
export default Comment = ({ id, user, text, onDelete, logined }) => {
  // 削除処理
  const deleteCommentClickHandler = async () => {
    if (confirm("このコメントを削除してもよろしいですか？")) {
      await axios.delete(`/api/comment/${id}/`);
    }
    onDelete(id);
  };

  return (
    <CommentContainer>
      <CommentHeader>
        <h6>{user.username}</h6>
        <span>　</span>
        <span>1日前</span>
        {logined && <CommentDeleteButton onClick={deleteCommentClickHandler}>削除</CommentDeleteButton>}

      </CommentHeader>
      <CommentText>{text}</CommentText>
      <CommentFooter />
    </CommentContainer>
  );
};
