// src/components/molecules/SignUpLink.js
import CustomLink from '../../atoms/CustomLink';

function SignUpLink(props) {
    return (
        <CustomLink href="#" {...props}>
            {"Don't have an account? Sign Up"}
        </CustomLink>
    );
}

export default SignUpLink;
