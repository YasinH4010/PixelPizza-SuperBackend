const Item = require(`${__dirname}/../Models/itemModel`)
const Order = require("../Models/orderModel")
const User = require(`${__dirname}/../Models/userModel`)

exports.statsSummary = async function (req, res) {
  try {
    const startOfMonth = new Date();
    startOfMonth.setDate(1);
    startOfMonth.setHours(0, 0, 0, 0);

    // کاربران جدید این ماه
    const newUsersThisMonth = await User.countDocuments({
      joinedAt: { $gte: startOfMonth }
    });

    // سفارش‌های این ماه
    const ordersThisMonth = await Order.find({
      createdAt: { $gte: startOfMonth }
    });

    const totalOrdersThisMonth = ordersThisMonth.length;
    const totalPaidThisMonth = ordersThisMonth.reduce((sum, o) => sum + (o.paid || 0), 0);

    // بیشترین کاربر سفارش‌دهنده این ماه
    const topUserAgg = await Order.aggregate([
      { $match: { createdAt: { $gte: startOfMonth } } },
      { $group: { _id: "$orderer", orders: { $sum: 1 }, totalSpent: { $sum: "$paid" } } },
      { $sort: { totalSpent: -1 } },
      { $limit: 1 },
      {
        $lookup: {
          from: "users",
          localField: "_id",
          foreignField: "_id",
          as: "user"
        }
      },
      { $unwind: "$user" },
      { $project: { _id: 0, user: { _id: "$user._id", name: "$user.name" }, totalSpent: 1, orders: 1 } }
    ]);
    const topUser = topUserAgg[0] || null;

    // آیتم‌های پر فروش این ماه (چون داخل items کل object هست، مستقیم همونجا group می‌کنیم)
    const topItemsAgg = await Order.aggregate([
      { $match: { createdAt: { $gte: startOfMonth } } },
      { $unwind: "$items" },
      { $group: { _id: "$items.item._id", name: { $first: "$items.item.name" }, count: { $sum: 1 } } },
      { $sort: { count: -1 } },
      { $limit: 3 },
      { $project: { _id: 0, item: { _id: "$_id", name: "$name" }, count: 1 } }
    ]);

    // 3 کاربر پر خرید (کل دیتابیس)
    const topUsersOverall = await Order.aggregate([
      { $group: { _id: "$orderer", orders: { $sum: 1 }, totalSpent: { $sum: "$paid" } } },
      { $sort: { totalSpent: -1 } },
      { $limit: 3 },
      {
        $lookup: {
          from: "users",
          localField: "_id",
          foreignField: "_id",
          as: "user"
        }
      },
      { $unwind: "$user" },
      { $project: { _id: 0, user: { _id: "$user._id", name: "$user.name" }, totalSpent: 1, orders: 1 } }
    ]);

    res.json({
      status: "success",
      data: {
        newUsersThisMonth,
        totalOrdersThisMonth,
        totalPaidThisMonth,
        topUser,
        topItems: topItemsAgg,
        topUsersOverall
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ status: "error", message: err.message });
  }
};

