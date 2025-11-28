// frontend\src\utils\cookies\CookieUtils.js

import Cookies from 'js-cookie';

class CookieUtils {

    static setUserCookie(user, expiresDays = 7) {
        try {
            const stringified = JSON.stringify(user);
            const encoded = encodeURIComponent(stringified);
            Cookies.set('user', encoded, { expires: expiresDays });
        } catch (error) {
            console.error('Error setting user cookie', error);
        }
    }

    static getUserCookie() {
        const cookieUser = Cookies.get('user');
        if (cookieUser) {
            try {
                const decoded = decodeURIComponent(cookieUser);
                return JSON.parse(decoded);
            } catch (error) {
                console.error('Error parsing user cookie', error);
            }
        }
        return null;
    }

    static removeUserCookie() {
        try {
            Cookies.remove('user');
        } catch (error) {
            console.error('Error removing user cookie', error);
        }
    }
}

export default CookieUtils;
