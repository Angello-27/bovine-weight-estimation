// src/components/molecules/ForgotPasswordLink.js
import CustomLink from '../../atoms/CustomLink';

function ForgotPasswordLink(props) {
    return (
        <CustomLink href="#" {...props}>
            Forgot password?
        </CustomLink>
    );
}

export default ForgotPasswordLink;
