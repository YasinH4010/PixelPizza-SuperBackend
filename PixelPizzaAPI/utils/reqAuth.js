const { updateUserLastSeen, protect, restrictTo } = require("../Controller/authController");

const withAuth = (...permissions) => [
  updateUserLastSeen,
  protect,
  restrictTo(...permissions),
];

module.exports = withAuth