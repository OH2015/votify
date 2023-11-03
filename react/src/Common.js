import styled from "styled-components";

export const PopupOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  background-color: rgba(0, 0, 0, 0.5);
`;

export const PopupContent = styled.div`
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
