import React from "react";
import styled from "styled-components";

const CommentContainer = styled.div`
  margin-top: 20px;
`;
const CommentHeader = styled.div`
  display: flex;
`;
const DispDate = styled.span`
  font-size: 12px;
  margin-left: 20px;
`;
const CommentDeleteButton = styled.span`
  margin-left: auto;
  margin-right: 10px;
  border: none;
  background-color: transparent;
  cursor: pointer;
  font-size: 12px;
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
export default Comment = ({ id, user, text, disp_date, onDelete, userId }) => {
  // 削除処理
  const deleteCommentClickHandler = async () => {
    if (confirm("このコメントを削除してもよろしいですか？")) {
      await axios.delete(`/api/comment/${id}/`);
      onDelete(id);
    }
  };

  return (
    <CommentContainer>
      <CommentHeader>
        <h6>{user.username}</h6>
        <DispDate>{disp_date}</DispDate>
        {userId === user.id && (
          <CommentDeleteButton onClick={deleteCommentClickHandler}>
            削除
          </CommentDeleteButton>
        )}
      </CommentHeader>
      <CommentText>{text}</CommentText>
      <CommentFooter />
    </CommentContainer>
  );
};
