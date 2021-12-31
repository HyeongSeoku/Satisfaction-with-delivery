import React, { useEffect } from "react";
import styled from "styled-components";
import Logo from "./Logo";
import LogoSrc from "../img/chef.png";

const MytownHeader = styled.div`
  width: 100%;
  height: 150px;
  flex-grow: 2;
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 20px 20px 20px 30px;
  box-sizing: border-box;
  border-bottom: 1px solid;
`;

const HedaerLogo = styled(Logo)`
  flex-grow: 1;
`;

const EmptyDiv = styled.div`
  flex-grow: 30;
`;

const LogoImg = styled.img`
  width: 130px;
  height: 100%;
  margin-right: 20px;
`;

const MenuHeader = () => {
  return (
    <MytownHeader>
      <HedaerLogo logoWidth="50px" logoHeight="50px" logoFontSize="43px" />
      <EmptyDiv />
      <LogoImg src={LogoSrc} />
    </MytownHeader>
  );
};

export default MenuHeader;
