import Header from "./Header";
import Login from "./Login";
import Register from "./Register";
import RegisterComplete from "./RegisterComplete";
import PasswordResetMail from "./PasswordResetMail";
import PasswordReset from "./PasswordReset";
import PasswordChange from "./PasswordChange";
import QuestionCreate from "./QuestionCreate";
import "./style.css";
import { BrowserRouter, Link, Routes, Route } from "react-router-dom";
import AccountInfo from "./AccountInfo";
import Top from "./top/Top";

function App() {
  return (
    <>
      <BrowserRouter>
        <Header></Header>
        <div id="main_content">
          <div className="content_center">
            <Routes>
              <Route path="/" element={<Top />} />
              <Route path="/login" element={<Login />} />
              <Route path="/account_info" element={<AccountInfo />} />
              <Route path="/account_register" element={<Register />} />
              <Route
                path="/account_register_complete"
                element={<RegisterComplete />}
              />
              <Route
                path="/password_reset_mail"
                element={<PasswordResetMail />}
              />
              <Route path="/password_reset" element={<PasswordReset />} />
              <Route path="/password_change" element={<PasswordChange />} />
              <Route path="/question_create" element={<QuestionCreate />} />
            </Routes>
          </div>
        </div>
        <footer id="footer" className="footer outer-block">
          <div className="logo">
            <Link to="/">
              <img src="./logo_transparent.png"></img>
            </Link>
          </div>
          <ul className="nav">
            <li>
              <a
                href="https://docs.google.com/forms/d/e/1FAIpQLSdTPn1bsOk2LXV3JlKGnLv6zDZxzva85Q6XY9gc2itfKwTxEw/viewform?usp=sf_link"
                target="_blank"
                rel="noopener noreferrer"
              >
                問い合わせ
              </a>
            </li>
          </ul>
          <div>COPYRIGHT © Votify Inc. All rights Reserved.</div>
        </footer>
      </BrowserRouter>
    </>
  );
}
export default App;
