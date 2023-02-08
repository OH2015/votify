'use strict';

import { createRoot } from 'react-dom/client';
import React from 'react'
import Body from './Body'

// ルートコンポーネント
const Root = () => {
    return (
        <Body />
    );
}

const root = createRoot(document.getElementById('root'));
root.render(Root());