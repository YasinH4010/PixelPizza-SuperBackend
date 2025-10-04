const nodemailer = require('nodemailer')

const sendEmail = async options => {
    console.log('EMAIL_HOST:', process.env.EMAIL_HOST);
    console.log('EMAIL_PORT:', process.env.EMAIL_PORT);
console.log('EMAIL_NAME:', process.env.EMAIL_NAME);
console.log('EMAIL_PASS:', process.env.EMAIL_PASS);

    const transporter = nodemailer.createTransport({
        host: process.env.EMAIL_HOST,
        port: process.env.EMAIL_PORT,
        auth: {
            user: process.env.EMAIL_NAME,
            pass: process.env.EMAIL_PASS
        }
    })

    const mailOptions = {
        from: `PixelPizzaAPI <${process.env.EMAIL_NAME}>`,
        to: options.email,
        subject: options.subject,
        text: options.message
    }

    await transporter.sendMail(mailOptions)
}

module.exports = sendEmail